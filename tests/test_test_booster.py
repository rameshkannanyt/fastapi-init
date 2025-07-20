import pytest
from fastapi_kickstart.test_booster import TestBooster

@pytest.fixture
def test_booster():
    return TestBooster()

def test_async_test_setup(test_booster):
    assert test_booster.setup_async_test_harness() is True

def test_example_test_case(test_booster):
    result = test_booster.run_example_test()
    assert result == "Example test passed!"

def test_booster_integration(test_booster):
    assert test_booster.integrate_with_fastapi() is True

def test_cleanup(test_booster):
    assert test_booster.cleanup() is True