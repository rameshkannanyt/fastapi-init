import pytest
from fastapi_kickstart.async_analyzer import AsyncAnalyzer

@pytest.fixture
def analyzer():
    return AsyncAnalyzer()

def test_analyze_async_function(analyzer):
    async def async_function():
        return "Hello, World!"

    result = analyzer.analyze(async_function)
    assert result['is_async'] is True
    assert result['issues'] == []

def test_analyze_sync_function(analyzer):
    def sync_function():
        return "Hello, World!"

    result = analyzer.analyze(sync_function)
    assert result['is_async'] is False
    assert 'Blocking function detected' in result['issues']

def test_analyze_mixed_function(analyzer):
    async def mixed_function():
        return sync_function()

    def sync_function():
        return "Hello, World!"

    result = analyzer.analyze(mixed_function)
    assert result['is_async'] is True
    assert 'Blocking function detected' in result['issues']

def test_analyze_with_blocking_call(analyzer):
    async def async_function_with_blocking_call():
        return blocking_call()

    def blocking_call():
        return "Blocking call"

    result = analyzer.analyze(async_function_with_blocking_call)
    assert result['is_async'] is True
    assert 'Blocking function detected' in result['issues']