"""Core functionality for the FastAPI Kickstart toolkit."""

from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, DictLoader

from .templates import TEMPLATES
from .utils import logger
from .scaffolder import ProjectScaffolder
from .env_checker import EnvironmentChecker
from .async_analyzer import AsyncAnalyzer
from .error_middleware import ErrorMiddleware
from .test_booster import TestBooster
from .onboarding import OnboardingReport


class FastAPIKickstart:
    """Main class for the FastAPI Kickstart toolkit."""

    def __init__(self):
        self.template_env = Environment(loader=DictLoader(TEMPLATES))
        self.scaffolder = ProjectScaffolder()
        self.env_checker = EnvironmentChecker()
        self.async_analyzer = AsyncAnalyzer()
        self.error_middleware = ErrorMiddleware()
        self.test_booster = TestBooster()
        self.onboarding_report = OnboardingReport()

    def init_project(self, project_name: str, base_path: Path):
        """Initialize a new FastAPI project."""
        return self.scaffolder.create_project_scaffold(project_name, base_path)

    def check_environment(self, project_path: Path):
        """Check the environment for missing dependencies."""
        return self.env_checker.check_environment(project_path)

    def analyze_async_code(self, project_path: Path):
        """Analyze the project for async/sync issues."""
        return self.async_analyzer.analyze(project_path)

    def add_error_handling(self, project_path: Path):
        """Add error handling middleware to the project."""
        return self.error_middleware.add_to_project(project_path)

    def setup_testing(self, project_path: Path):
        """Set up testing for the project."""
        return self.test_booster.setup(project_path)

    def generate_onboarding_report(self, project_path: Path) -> Path:
        """Generate an onboarding report for the project."""
        return self.onboarding_report.generate(project_path)