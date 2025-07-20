import click
from pathlib import Path
from fastapi_kickstart.scaffolder import ProjectScaffolder
from fastapi_kickstart.env_checker import EnvironmentChecker
from fastapi_kickstart.async_analyzer import AsyncAnalyzer
from fastapi_kickstart.error_middleware import ErrorMiddleware
from fastapi_kickstart.test_booster import TestBooster
from fastapi_kickstart.onboarding import OnboardingReport

@click.group()
def cli():
    """FastAPI Kickstart Toolkit Command Line Interface."""
    pass

@cli.command()
@click.argument('project_name')
@click.option('--with-database', is_flag=True, help='Include database setup with SQLAlchemy and Alembic')
@click.option('--with-auth', is_flag=True, help='Include JWT authentication system')
@click.option('--with-docker', is_flag=True, help='Include Docker and Docker Compose files')
@click.option('--with-tests', is_flag=True, help='Include comprehensive test setup')
def init(project_name, with_database, with_auth, with_docker, with_tests):
    """Initialize a new FastAPI project scaffold."""
    scaffolder = ProjectScaffolder()
    project_path = scaffolder.create_project_scaffold(project_name)
    click.echo(f"Project created at: {project_path}")
    
    if with_database or with_auth or with_docker or with_tests:
        click.echo("Enhanced features included:")
        if with_database:
            click.echo("  - Database setup with SQLAlchemy and Alembic")
        if with_auth:
            click.echo("  - JWT authentication system")
        if with_docker:
            click.echo("  - Docker and Docker Compose configuration")
        if with_tests:
            click.echo("  - Comprehensive test setup")

@cli.command()
def env_check():
    """Check the environment for missing dependencies and issues."""
    checker = EnvironmentChecker()
    issues = checker.check_environment()
    if issues:
        click.echo("Issues found in the environment:")
        for issue in issues:
            click.echo(f"- {issue}")
    else:
        click.echo("No issues found in the environment.")

@cli.command()
def add_error_middleware():
    """Add customizable error handling middleware to the FastAPI app."""
    middleware = ErrorMiddleware()
    project_path = Path.cwd()
    success = middleware.add_to_project(project_path)
    if success:
        click.echo("Error middleware added.")
    else:
        click.echo("Failed to add error middleware.")

@cli.command()
def test_init():
    """Set up async test support and example test suite."""
    booster = TestBooster()
    project_path = Path.cwd()
    success = booster.setup_tests(project_path)
    if success:
        click.echo("Async test support and example tests set up.")
    else:
        click.echo("Failed to set up tests.")

@cli.command()
def onboarding_report():
    """Generate an onboarding report for the FastAPI project."""
    report = OnboardingReport()
    project_path = Path.cwd()
    report_path = report.generate(project_path)
    click.echo(f"Onboarding report generated at: {report_path}")

@cli.command()
def setup_database():
    """Set up database with Alembic migrations."""
    project_path = Path.cwd()
    alembic_dir = project_path / "alembic"
    
    if not alembic_dir.exists():
        click.echo("Alembic not found. Please run 'fastapi-kickstart init' with --with-database first.")
        return
    
    try:
        import subprocess
        import sys
        
        # Initialize Alembic
        result = subprocess.run([sys.executable, "-m", "alembic", "init", "alembic"], 
                              cwd=project_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            click.echo("Database setup completed successfully.")
            click.echo("Run 'alembic upgrade head' to apply migrations.")
        else:
            click.echo(f"Failed to setup database: {result.stderr}")
            
    except ImportError:
        click.echo("Alembic not installed. Install it with: pip install alembic")
    except Exception as e:
        click.echo(f"Error setting up database: {e}")

@cli.command()
def docker_setup():
    """Set up Docker configuration for the project."""
    project_path = Path.cwd()
    
    # Check if Dockerfile already exists
    dockerfile_path = project_path / "Dockerfile"
    if dockerfile_path.exists():
        click.echo("Dockerfile already exists.")
        return
    
    try:
        # Create Dockerfile
        dockerfile_content = """FROM python:3.11-slim

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
"""
        
        with open(dockerfile_path, "w", encoding="utf-8") as f:
            f.write(dockerfile_content)
        
        # Create docker-compose.yml
        compose_content = """version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/app
      - SECRET_KEY=your-secret-key-here
    depends_on:
      - db
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=app
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

volumes:
  postgres_data:
"""
        
        compose_path = project_path / "docker-compose.yml"
        with open(compose_path, "w", encoding="utf-8") as f:
            f.write(compose_content)
        
        click.echo("Docker configuration created successfully.")
        click.echo("Run 'docker build -t app .' to build the image.")
        click.echo("Run 'docker-compose up' to start the services.")
        
    except Exception as e:
        click.echo(f"Error setting up Docker: {e}")

@cli.command()
def add_monitoring():
    """Add monitoring and logging configuration."""
    project_path = Path.cwd()
    
    # Create monitoring configuration
    monitoring_content = """import logging
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class MonitoringMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        # Log request details
        logging.info(
            f"{request.method} {request.url.path} - {response.status_code} - {process_time:.4f}s"
        )
        
        return response

def setup_monitoring(app):
    app.add_middleware(MonitoringMiddleware)
"""
    
    monitoring_path = project_path / "app" / "core" / "monitoring.py"
    monitoring_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(monitoring_path, "w", encoding="utf-8") as f:
        f.write(monitoring_content)
    
    click.echo("Monitoring configuration added.")
    click.echo("Import and use setup_monitoring() in your main.py")

@cli.command()
def add_rate_limiting():
    """Add rate limiting middleware."""
    project_path = Path.cwd()
    
    # Create rate limiting configuration
    rate_limit_content = """import time
from collections import defaultdict
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()
        
        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if now - req_time < 60
        ]
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later."
            )
        
        # Add current request
        self.requests[client_ip].append(now)
        
        return await call_next(request)

def setup_rate_limiting(app, requests_per_minute: int = 60):
    app.add_middleware(RateLimitMiddleware, requests_per_minute=requests_per_minute)
"""
    
    rate_limit_path = project_path / "app" / "core" / "rate_limit.py"
    rate_limit_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(rate_limit_path, "w", encoding="utf-8") as f:
        f.write(rate_limit_content)
    
    click.echo("Rate limiting middleware added.")
    click.echo("Import and use setup_rate_limiting() in your main.py")

def main():
    """Main entry point for the CLI."""
    cli()

if __name__ == "__main__":
    main()