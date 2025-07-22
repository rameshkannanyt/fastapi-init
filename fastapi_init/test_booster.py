from fastapi import FastAPI
from fastapi.testclient import TestClient
from pathlib import Path
import pytest

class TestBooster:
    """Provides testing utilities and setup for FastAPI projects."""
    
    def __init__(self):
        pass
    
    def setup_tests(self, project_path: Path = None) -> bool:
        """Set up async test support and example test suite."""
        if project_path is None:
            project_path = Path.cwd()
        
        try:
            # Create test files
            self._create_test_files(project_path)
            return True
        except Exception as e:
            print(f"Failed to setup tests: {e}")
            return False
    
    def setup(self, project_path: Path) -> bool:
        """Set up testing for the project."""
        return self.setup_tests(project_path)
    
    def _create_test_files(self, project_path: Path):
        """Create test files for the project."""
        tests_dir = project_path / "tests"
        tests_dir.mkdir(exist_ok=True)
        
        # Create conftest.py
        conftest_content = '''import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def app_instance():
    return app
'''
        
        conftest_file = tests_dir / "conftest.py"
        with open(conftest_file, "w", encoding="utf-8") as f:
            f.write(conftest_content)
        
        # Create test_main.py
        test_main_content = '''import pytest
from fastapi.testclient import TestClient

def test_root_endpoint(client: TestClient):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

def test_health_endpoint(client: TestClient):
    """Test the health check endpoint."""
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_docs_endpoint(client: TestClient):
    """Test that the docs endpoint is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200
'''
        
        test_main_file = tests_dir / "test_main.py"
        with open(test_main_file, "w", encoding="utf-8") as f:
            f.write(test_main_content)
        
        # Create test_api directory and test_health.py
        test_api_dir = tests_dir / "api"
        test_api_dir.mkdir(exist_ok=True)
        
        test_health_content = '''import pytest
from fastapi.testclient import TestClient

def test_health_check(client: TestClient):
    """Test the health check endpoint."""
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

@pytest.mark.asyncio
async def test_health_check_async(client: TestClient):
    """Test the health check endpoint asynchronously."""
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
'''
        
        test_health_file = test_api_dir / "test_health.py"
        with open(test_health_file, "w", encoding="utf-8") as f:
            f.write(test_health_content)
        
        # Create pytest.ini
        pytest_ini_content = '''[tool:pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
'''
        
        pytest_ini_file = project_path / "pytest.ini"
        with open(pytest_ini_file, "w", encoding="utf-8") as f:
            f.write(pytest_ini_content)


# Legacy code for backward compatibility
# Create a FastAPI instance for testing
app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Test client for making requests to the FastAPI app
client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

# Additional test cases can be added here
# This file is intentionally left blank for future test cases.