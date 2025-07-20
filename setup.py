from setuptools import setup, find_packages
import os

# Read README with proper encoding
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except (FileNotFoundError, UnicodeDecodeError):
        return "A comprehensive toolkit for kickstarting FastAPI projects with best practices."

setup(
    name="fastapi-kickstart",
    version="0.2.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive toolkit for kickstarting FastAPI projects with best practices.",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fastapi-kickstart",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi>=0.100",
        "uvicorn[standard]",
        "jinja2",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "sqlalchemy>=2.0.0",
        "alembic>=1.12.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.6",
        "email-validator>=2.0.0",
        "httpx",
        "pytest",
        "pytest-asyncio",
        "click",
    ],
    extras_require={
        "dev": [
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "pytest-xdist>=3.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "mkdocs>=1.4.0",
            "mkdocs-material>=9.0.0",
            "pre-commit>=3.0.0",
        ],
        "database": [
            "psycopg2-binary>=2.9.0",
            "asyncpg>=0.28.0",
        ],
        "monitoring": [
            "prometheus-client>=0.16.0",
            "structlog>=23.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Framework :: FastAPI",
        "Typing :: Typed",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'fastapi-kickstart=fastapi_kickstart.cli:main',
        ],
    },
    keywords="fastapi, scaffolding, toolkit, web, api, framework",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/fastapi-kickstart/issues",
        "Source": "https://github.com/yourusername/fastapi-kickstart",
        "Documentation": "https://github.com/yourusername/fastapi-kickstart#readme",
    },
)