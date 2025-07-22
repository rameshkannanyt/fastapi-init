import pytest
from fastapi_init.scaffolder import FastAPIKickstart

@pytest.fixture
def fastapi_init():
    return FastAPIKickstart()

def test_create_project_scaffold(fastapi_init, tmp_path):
    project_name = "test_project"
    project_path = tmp_path / project_name

    # Create project scaffold
    result_path = fastapi_init.create_project_scaffold(project_name, base_path=tmp_path)

    # Check if the project path was created
    assert result_path == project_path
    assert project_path.exists()

    # Check if the necessary directories were created
    assert (project_path / "app").exists()
    assert (project_path / "tests").exists()
    assert (project_path / "requirements.txt").exists()

def test_create_project_scaffold_existing_directory(fastapi_init, tmp_path):
    project_name = "existing_project"
    project_path = tmp_path / project_name
    project_path.mkdir()

    # Attempt to create a project scaffold in an existing directory
    with pytest.raises(ValueError, match=f"Project directory {project_path} already exists"):
        fastapi_init.create_project_scaffold(project_name, base_path=tmp_path)

def test_generate_files(fastapi_init, tmp_path):
    project_name = "test_project"
    project_path = tmp_path / project_name
    fastapi_init.create_project_scaffold(project_name, base_path=tmp_path)

    # Check if specific files were generated
    assert (project_path / "app" / "main.py").exists()
    assert (project_path / "app" / "core" / "config.py").exists()
    assert (project_path / "README.md").exists()