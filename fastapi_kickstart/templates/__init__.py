# Templates for FastAPI project scaffolding
TEMPLATES = {
    "main.py": """from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1.router import api_router
from app.core.middleware import ErrorMiddleware
from app.core.logging import setup_logging

# Create database tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    setup_logging()
    yield
    # Shutdown
    pass

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=settings.description,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add error handling middleware
app.add_middleware(ErrorMiddleware)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.version,
        "docs": "/docs",
        "health": "/api/v1/health/"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.app_name}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
""",

    "config.py": """from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # App settings
    app_name: str = "{{ project_name }}"
    version: str = "1.0.0"
    description: str = "A FastAPI application created with fastapi-kickstart"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Security
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database
    database_url: str = "sqlite:///./app.db"
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "app.log"
    
    # Rate limiting
    rate_limit_per_minute: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
""",

    "database.py": """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""",

    "models.py": """from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
""",

    "schemas.py": """from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
""",

    "auth.py": """from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.models import User
from app.schemas.schemas import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
""",

    "auth_router.py": """from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.core.auth import verify_password, create_access_token, get_current_active_user
from app.models.models import User
from app.schemas.schemas import Token, User as UserSchema

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
""",

    "router.py": """from fastapi import APIRouter
from .health import router as health_router
from .auth_router import router as auth_router

api_router = APIRouter()

api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(auth_router, tags=["authentication"])
""",

    "health.py": """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()

@router.get("/")
async def health_check():
    return {"status": "healthy"}

@router.get("/db")
async def database_health_check(db: Session = Depends(get_db)):
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}
""",

    "logging.py": """import logging
import sys
from pathlib import Path
from app.core.config import settings

def setup_logging():
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(settings.log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
""",

    "requirements.txt": """fastapi>=0.100.0
uvicorn[standard]>=0.20.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
sqlalchemy>=2.0.0
alembic>=1.12.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6
email-validator>=2.0.0
pytest>=7.0.0
pytest-asyncio>=0.21.0
httpx>=0.24.0
""",

    "README.md": """# {{ project_name }}

A FastAPI application created with fastapi-kickstart.

## Features

- 🔐 JWT Authentication
- 🗄️ SQLAlchemy ORM with Alembic migrations
- 📝 Automatic API documentation
- 🧪 Comprehensive testing setup
- 🐳 Docker support
- 📊 Health checks
- 🔒 CORS configuration
- 📝 Structured logging

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### Database Setup

```bash
# Initialize database
alembic upgrade head
```

### Running the Application

```bash
# Development
uvicorn app.main:app --reload

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Project Structure

```
{{ project_name }}/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth_router.py
│   │       ├── health.py
│   │       └── router.py
│   ├── core/
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── logging.py
│   │   └── middleware.py
│   ├── models/
│   │   └── models.py
│   ├── schemas/
│   │   └── schemas.py
│   └── main.py
├── tests/
├── alembic/
├── logs/
└── requirements.txt
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py -v
```

## Docker

```bash
# Build image
docker build -t {{ project_name }} .

# Run container
docker run -p 8000:8000 {{ project_name }}
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

- `SECRET_KEY`: JWT secret key
- `DATABASE_URL`: Database connection string
- `DEBUG`: Enable debug mode
- `ALLOWED_ORIGINS`: CORS allowed origins
""",

    "Dockerfile": """FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""",

    "docker-compose.yml": """version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/{{ project_name }}
      - SECRET_KEY=your-secret-key-here
    depends_on:
      - db
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB={{ project_name }}
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

volumes:
  postgres_data:
""",

    ".env.example": """# Application Settings
APP_NAME={{ project_name }}
VERSION=1.0.0
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=sqlite:///./app.db
# For PostgreSQL: postgresql://user:password@localhost/{{ project_name }}

# CORS
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:8080"]

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
""",

    "alembic.ini": """[alembic]
script_location = alembic
sqlalchemy.url = sqlite:///./app.db

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
""",

    "alembic_env.py": """from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from app.core.config import settings
from app.models.models import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_url():
    return settings.database_url

def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
""",

    "pytest.ini": """[tool:pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
""",

    ".gitignore": """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# poetry
poetry.lock

# pdm
.pdm.toml

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
.idea/

# VS Code
.vscode/

# Database
*.db
*.sqlite
*.sqlite3

# Logs
logs/
*.log

# OS
.DS_Store
Thumbs.db
""",

    "Makefile": """# Makefile for {{ project_name }}

.PHONY: help install test run clean docker-build docker-run

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=app --cov-report=html

run: ## Run the application
	uvicorn app.main:app --reload

run-prod: ## Run the application in production mode
	uvicorn app.main:app --host 0.0.0.0 --port 8000

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

docker-build: ## Build Docker image
	docker build -t {{ project_name }} .

docker-run: ## Run Docker container
	docker run -p 8000:8000 {{ project_name }}

docker-compose-up: ## Start services with Docker Compose
	docker-compose up -d

docker-compose-down: ## Stop services with Docker Compose
	docker-compose down

migrate: ## Run database migrations
	alembic upgrade head

migrate-create: ## Create new migration
	alembic revision --autogenerate -m "$(message)"

format: ## Format code with black
	black app/ tests/

lint: ## Lint code with flake8
	flake8 app/ tests/

type-check: ## Type check with mypy
	mypy app/
""",

    "requirements-dev.txt": """# Development dependencies
-r requirements.txt

# Testing
pytest-cov>=4.0.0
pytest-mock>=3.10.0
pytest-xdist>=3.0.0

# Code quality
black>=23.0.0
flake8>=6.0.0
isort>=5.12.0
mypy>=1.0.0

# Documentation
mkdocs>=1.4.0
mkdocs-material>=9.0.0

# Pre-commit
pre-commit>=3.0.0
""",

    ".pre-commit-config.yaml": """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203,W503]
""",

    "mkdocs.yml": """site_name: {{ project_name }} API Documentation
site_description: API documentation for {{ project_name }}
site_author: Your Name
site_url: https://your-domain.com

repo_name: your-username/{{ project_name }}
repo_url: https://github.com/your-username/{{ project_name }}

theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - search.suggest
    - search.highlight

nav:
  - Home: index.md
  - API Reference: api.md
  - Authentication: auth.md
  - Examples: examples.md

plugins:
  - search
  - mkdocstrings:
      default_handler: python
      handlers:
        python:
          paths: [app]
          options:
            show_source: true
            show_root_heading: true

markdown_extensions:
  - admonition
  - codehilite
  - pymdownx.superfences
  - pymdownx.tabbed
  - toc:
      permalink: true
""",
}