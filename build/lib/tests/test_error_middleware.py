import pytest
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi_init.error_middleware import ErrorMiddleware

app = FastAPI()

# Sample route to demonstrate error handling
@app.get("/error")
async def error_route():
    raise HTTPException(status_code=400, detail="This is a test error.")

# Add the error middleware
app.add_middleware(ErrorMiddleware)

@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    return TestClient(app)

def test_error_handling(client):
    response = client.get("/error")
    assert response.status_code == 400
    assert response.json() == {"detail": "This is a test error."}

def test_custom_error_response(client):
    # Simulate a custom error response
    @app.get("/custom-error")
    async def custom_error_route():
        raise HTTPException(status_code=500, detail="Custom error occurred.")

    response = client.get("/custom-error")
    assert response.status_code == 500
    assert response.json() == {"detail": "Custom error occurred."}