from pathlib import Path
from typing import Dict, Any
from fastapi_init.templates import TEMPLATES
from jinja2 import Environment, DictLoader

class ProjectScaffolder:
    """Handles the creation of the project structure and files based on templates."""

    def __init__(self):
        # Use the shared TEMPLATES dictionary for all templates
        self.template_env = Environment(loader=DictLoader(TEMPLATES))

    def create_project_scaffold(self, project_name: str, base_path: Path = None) -> Path:
        """Create a new FastAPI project scaffold."""
        if base_path is None:
            base_path = Path.cwd()
        
        project_path = base_path / project_name
        config = {"project_name": project_name}
        
        self.create_project_structure(project_path, config)
        return project_path

    def create_project_structure(self, project_path: Path, config: Dict[str, Any]):
        """Create the project directory structure and generate files from templates."""
        self._create_directory_structure(project_path)
        self._generate_files(project_path, config)
        self._setup_alembic(project_path, config)

    def _create_directory_structure(self, project_path: Path):
        """Create the project directory structure."""
        directories = [
            "",  # root
            "app",
            "app/api",
            "app/api/v1",
            "app/core",
            "app/models",
            "app/schemas",
            "app/services",
            "app/utils",
            "tests",
            "tests/api",
            "tests/utils",
            "tests/core",
            "tests/models",
            "scripts",
            "docs",
            "logs",
            "alembic",
            "alembic/versions",
        ]

        for dir_name in directories:
            dir_path = project_path / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)

            # Create __init__.py files for Python packages
            if dir_name.startswith("app") or dir_name.startswith("tests"):
                (dir_path / "__init__.py").touch()

    def _generate_files(self, project_path: Path, config: Dict[str, Any]):
        """Generate project files from templates."""
        file_mapping = {
            "main.py": "app/main.py",
            "config.py": "app/core/config.py",
            "database.py": "app/core/database.py",
            "auth.py": "app/core/auth.py",
            "logging.py": "app/core/logging.py",
            "middleware.py": "app/core/middleware.py",
            "models.py": "app/models/models.py",
            "schemas.py": "app/schemas/schemas.py",
            "router.py": "app/api/v1/router.py",
            "health.py": "app/api/v1/health.py",
            "auth_router.py": "app/api/v1/auth_router.py",
            "requirements.txt": "requirements.txt",
            "README.md": "README.md",
            "Dockerfile": "Dockerfile",
            "docker-compose.yml": "docker-compose.yml",
            ".env.example": ".env.example",
            "pytest.ini": "pytest.ini",
            ".gitignore": ".gitignore",
            "Makefile": "Makefile",
            "requirements-dev.txt": "requirements-dev.txt",
            ".pre-commit-config.yaml": ".pre-commit-config.yaml",
        }

        # Generate each file
        for template_name, file_path in file_mapping.items():
            try:
                template = self.template_env.get_template(template_name)
                content = template.render(**config)

                full_path = project_path / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)

                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(content)

            except Exception as e:
                raise RuntimeError(f"Failed to generate {file_path}: {e}") from e

    def _setup_alembic(self, project_path: Path, config: Dict[str, Any]):
        """Set up Alembic for database migrations."""
        try:
            # Create alembic.ini
            alembic_ini_content = self.template_env.get_template("alembic.ini").render(**config)
            alembic_ini_path = project_path / "alembic.ini"
            with open(alembic_ini_path, "w", encoding="utf-8") as f:
                f.write(alembic_ini_content)
            
            # Create alembic/env.py
            alembic_env_content = self.template_env.get_template("alembic_env.py").render(**config)
            alembic_env_path = project_path / "alembic" / "env.py"
            with open(alembic_env_path, "w", encoding="utf-8") as f:
                f.write(alembic_env_content)
            
            # Create alembic/script.py.mako
            script_mako_content = """\"\"\"${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

\"\"\"
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
"""
            script_mako_path = project_path / "alembic" / "script.py.mako"
            with open(script_mako_path, "w", encoding="utf-8") as f:
                f.write(script_mako_content)
                
        except Exception as e:
            raise RuntimeError(f"Failed to setup Alembic: {e}") from e