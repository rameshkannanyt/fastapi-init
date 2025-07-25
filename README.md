# FastAPI Init Project 🚀

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive toolkit for kickstarting FastAPI projects with best practices, production-ready configurations, and modern development tools.

- **GitHub:** [rameshkannanyt/fastapi-init](https://github.com/rameshkannanyt/fastapi-init)
- **Maintainer:** rameshkannanyt0078@gmail.com

---

## ✨ Features

- 🏗️ Project scaffolding with best-practice structure
- 🔐 JWT authentication & security
- 🗄️ SQLAlchemy ORM & Alembic migrations
- 🧪 Pytest-based test setup
- 🐳 Docker & Docker Compose support
- 📊 Health checks & onboarding reports
- 🔒 CORS & environment validation
- 📝 Structured logging
- 📚 Automatic API documentation

---

## 🚀 Quick Start

### Installation

```bash
pip install -e .
```

### Create a New Project

```bash
fastapi-init-project init my-api
# Options:
#   --with-database   Include database setup
#   --with-auth       Include JWT authentication
#   --with-docker     Include Docker & Compose
#   --with-tests      Include test setup

# Example:
fastapi-init-project init my-api --with-database --with-auth --with-docker --with-tests
```

### CLI Commands

```bash
fastapi-init-project init <project_name> [options]   # Scaffold a new project
fastapi-init-project env-check                      # Check environment for issues
fastapi-init-project onboarding-report              # Generate onboarding report
fastapi-init-project setup-database                 # Set up Alembic migrations
fastapi-init-project docker-setup                   # Add Docker configuration
```

---

## 📁 Project Structure

```
my-api/
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
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🧪 Testing

```bash
pytest
pytest --cov=app
```

---

## 🐳 Docker

```bash
docker build -t my-api .
docker run -p 8000:8000 my-api
docker-compose up -d
```

---

## ⚙️ Configuration

Copy `.env.example` to `.env` and edit as needed:
- `SECRET_KEY`: JWT secret key
- `DATABASE_URL`: Database connection string
- `DEBUG`: Enable debug mode
- `ALLOWED_ORIGINS`: CORS allowed origins

---

## 📚 Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

## 🤝 Contributing

Contributions are welcome! Please open issues or pull requests on [GitHub](https://github.com/rameshkannanyt/fastapi-init).

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

**Made with ❤️ for the FastAPI community**