import pytest
from fastapi_init.env_checker import check_environment

def test_check_environment(mocker):
    # Mock the functions that check for dependencies
    mock_check_pip = mocker.patch('fastapi_init.env_checker.check_pip')
    mock_check_poetry = mocker.patch('fastapi_init.env_checker.check_poetry')
    
    # Simulate the behavior of the environment checker
    mock_check_pip.return_value = True
    mock_check_poetry.return_value = True
    
    result = check_environment()
    
    assert result['pip'] is True
    assert result['poetry'] is True
    assert 'No issues found' in result['message']

def test_check_environment_missing_dependencies(mocker):
    # Mock the functions that check for dependencies
    mock_check_pip = mocker.patch('fastapi_init.env_checker.check_pip')
    mock_check_poetry = mocker.patch('fastapi_init.env_checker.check_poetry')
    
    # Simulate missing dependencies
    mock_check_pip.return_value = False
    mock_check_poetry.return_value = True
    
    result = check_environment()
    
    assert result['pip'] is False
    assert result['poetry'] is True
    assert 'Missing pip dependencies' in result['message']