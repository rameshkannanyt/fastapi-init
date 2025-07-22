from pathlib import Path
from typing import Dict, List, Any

class OnboardingReport:
    """Generates an onboarding report for FastAPI projects."""

    def __init__(self):
        pass

    def generate_report(self, project_path: Path = None) -> str:
        """Generate the onboarding report content."""
        if project_path is None:
            project_path = Path.cwd()
            
        report_data = {
            "project_name": project_path.name,
            "project_path": str(project_path),
            "routes": self._discover_routes(project_path),
            "dependencies": self._analyze_dependencies(project_path),
            "structure": self._analyze_structure(project_path),
            "issues": self._identify_issues(project_path),
        }
        return self._render_report(report_data)

    def generate(self, project_path: Path) -> Path:
        """Generate an onboarding report file and return the path."""
        report_content = self.generate_report(project_path)
        report_file = project_path / "ONBOARDING_REPORT.md"
        
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report_content)
        
        return report_file

    def _discover_routes(self, project_path: Path) -> List[Dict[str, str]]:
        """Discover FastAPI routes in the project."""
        routes = []
        
        # Look for main.py and router files
        main_file = project_path / "app" / "main.py"
        if main_file.exists():
            routes.append({"path": "/", "method": "GET", "description": "Root endpoint"})
            routes.append({"path": "/docs", "method": "GET", "description": "Interactive API documentation"})
            routes.append({"path": "/redoc", "method": "GET", "description": "ReDoc documentation"})
        
        # Look for health endpoint
        health_file = project_path / "app" / "api" / "v1" / "health.py"
        if health_file.exists():
            routes.append({"path": "/api/v1/health/", "method": "GET", "description": "Health check endpoint"})
        
        return routes

    def _analyze_dependencies(self, project_path: Path) -> List[str]:
        """Analyze project dependencies."""
        dependencies = []
        
        # Check requirements.txt
        requirements_file = project_path / "requirements.txt"
        if requirements_file.exists():
            with open(requirements_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        dependencies.append(line)
        
        # Check pyproject.toml
        pyproject_file = project_path / "pyproject.toml"
        if pyproject_file.exists():
            dependencies.append("pyproject.toml dependencies (check manually)")
        
        return dependencies if dependencies else ["fastapi", "uvicorn"]

    def _analyze_structure(self, project_path: Path) -> Dict[str, List[str]]:
        """Analyze project structure."""
        structure = {}
        
        # Analyze app directory
        app_dir = project_path / "app"
        if app_dir.exists():
            app_files = []
            for item in app_dir.rglob("*"):
                if item.is_file() and item.suffix == ".py":
                    app_files.append(str(item.relative_to(app_dir)))
            structure["app"] = app_files
        
        # Analyze tests directory
        tests_dir = project_path / "tests"
        if tests_dir.exists():
            test_files = []
            for item in tests_dir.rglob("*"):
                if item.is_file() and item.suffix == ".py":
                    test_files.append(str(item.relative_to(tests_dir)))
            structure["tests"] = test_files
        
        return structure if structure else {
            "app": ["main.py", "api", "core", "models", "schemas"],
            "tests": ["test_main.py", "test_health.py"],
        }

    def _identify_issues(self, project_path: Path) -> List[str]:
        """Identify potential issues in the project."""
        issues = []
        
        # Check for missing files
        if not (project_path / "app" / "main.py").exists():
            issues.append("No app/main.py file found")
        
        if not (project_path / "requirements.txt").exists():
            issues.append("No requirements.txt file found")
        
        if not (project_path / ".env.example").exists():
            issues.append("No .env.example file found")
        
        if not (project_path / "Dockerfile").exists():
            issues.append("No Dockerfile found")
        
        if not (project_path / "README.md").exists():
            issues.append("No README.md file found")
        
        return issues

    def _render_report(self, report_data: Dict[str, Any]) -> str:
        """Render the report in markdown format."""
        report_lines = [
            f"# Onboarding Report for {report_data['project_name']}",
            f"**Project Path:** {report_data['project_path']}",
            "",
            "## Routes",
        ]
        for route in report_data["routes"]:
            report_lines.append(f"- `{route['method']} {route['path']}`: {route['description']}")
        
        report_lines.append("")
        report_lines.append("## Dependencies")
        for dep in report_data["dependencies"]:
            report_lines.append(f"- {dep}")
        
        report_lines.append("")
        report_lines.append("## Project Structure")
        for folder, files in report_data["structure"].items():
            report_lines.append(f"### {folder}")
            for file in files:
                report_lines.append(f"- {file}")
        
        report_lines.append("")
        report_lines.append("## Issues")
        if report_data["issues"]:
            for issue in report_data["issues"]:
                report_lines.append(f"- {issue}")
        else:
            report_lines.append("- No issues found")

        return "\n".join(report_lines)