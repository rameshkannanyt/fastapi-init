import os
import sys
import subprocess
from pathlib import Path
from typing import List

class EnvironmentChecker:
    """Class to check the Python environment for missing dependencies and configuration issues."""

    def __init__(self):
        pass

    def check_environment(self, project_path: Path = None) -> List[str]:
        """Check for missing dependencies and return a list of issues."""
        if project_path is None:
            project_path = Path.cwd()
        
        issues = []
        
        # Check for missing dependencies
        missing_deps = self.check_dependencies(project_path)
        if missing_deps:
            issues.extend([f"Missing dependency: {dep}" for dep in missing_deps])
        
        # Check for common configuration issues
        config_issues = self.check_configuration(project_path)
        issues.extend(config_issues)
        
        return issues

    def check_dependencies(self, project_path: Path) -> List[str]:
        """Check for missing dependencies in requirements.txt and pyproject.toml."""
        requirements_file = project_path / "requirements.txt"
        pyproject_file = project_path / "pyproject.toml"

        missing_dependencies = []

        if requirements_file.exists():
            with open(requirements_file, "r") as f:
                required_packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]
                for package in required_packages:
                    if not self._is_package_installed(package):
                        missing_dependencies.append(package)

        if pyproject_file.exists():
            # Here you could add logic to check for dependencies in pyproject.toml
            pass

        return missing_dependencies

    def check_configuration(self, project_path: Path) -> List[str]:
        """Check for common configuration issues."""
        issues = []
        
        # Check if .env file exists
        env_file = project_path / ".env"
        if not env_file.exists():
            issues.append("No .env file found. Consider creating one for environment variables.")
        
        # Check if main.py exists
        main_file = project_path / "app" / "main.py"
        if not main_file.exists():
            issues.append("No app/main.py file found. This is required for a FastAPI application.")
        
        return issues

    def _is_package_installed(self, package: str) -> bool:
        """Check if a package is installed in the current environment."""
        try:
            subprocess.run([sys.executable, "-m", "pip", "show", package], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False

    def report_missing_dependencies(self, project_path: Path = None):
        """Report any missing dependencies to the user."""
        if project_path is None:
            project_path = Path.cwd()
            
        missing = self.check_dependencies(project_path)
        if missing:
            print("Missing dependencies:")
            for package in missing:
                print(f"- {package}")
            print("\nYou can install them using pip:")
            print(f"pip install {' '.join(missing)}")
        else:
            print("All dependencies are satisfied.")