import pytest
from fastapi_init.cli import main

def test_cli_init(mocker):
    mocker.patch('fastapi_init.cli.create_project_scaffold')
    project_name = "test_project"
    main(["init", project_name])
    fastapi_init.cli.create_project_scaffold.assert_called_once_with(project_name)

def test_cli_env_check(mocker):
    mocker.patch('fastapi_init.cli.check_environment')
    main(["env-check"])
    fastapi_init.cli.check_environment.assert_called_once()

def test_cli_add_error_middleware(mocker):
    mocker.patch('fastapi_init.cli.add_error_middleware')
    main(["add-error-middleware"])
    fastapi_init.cli.add_error_middleware.assert_called_once()

def test_cli_test_init(mocker):
    mocker.patch('fastapi_init.cli.setup_test_harness')
    main(["test-init"])
    fastapi_init.cli.setup_test_harness.assert_called_once()