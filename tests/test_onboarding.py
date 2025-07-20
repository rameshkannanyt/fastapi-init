import pytest
from fastapi_kickstart.onboarding import FastAPIOnboarding

@pytest.fixture
def onboarding_instance():
    return FastAPIOnboarding()

def test_generate_onboarding_report(onboarding_instance):
    project_path = "test_project"
    report_path = onboarding_instance.generate_onboarding_report(project_path)
    
    assert report_path.exists()
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    assert "project_name" in content
    assert "routes" in content
    assert "dependencies" in content
    assert "structure" in content
    assert "issues" in content

def test_discover_routes(onboarding_instance):
    project_path = "test_project"
    routes = onboarding_instance._discover_routes(project_path)
    
    assert isinstance(routes, list)
    assert len(routes) > 0
    assert all("path" in route for route in routes)

def test_analyze_dependencies(onboarding_instance):
    project_path = "test_project"
    dependencies = onboarding_instance._analyze_dependencies(project_path)
    
    assert isinstance(dependencies, list)
    assert len(dependencies) >= 0

def test_analyze_structure(onboarding_instance):
    project_path = "test_project"
    structure = onboarding_instance._analyze_structure(project_path)
    
    assert isinstance(structure, dict)
    assert len(structure) >= 0

def test_identify_issues(onboarding_instance):
    project_path = "test_project"
    issues = onboarding_instance._identify_issues(project_path)
    
    assert isinstance(issues, list)
    assert len(issues) >= 0