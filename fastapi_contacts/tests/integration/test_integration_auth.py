# fastapi_contacts/tests/integration/test_integration_auth.py
from fastapi.testclient import TestClient
from fastapi_contacts.main import app

client = TestClient(app)


def test_integration_login():
    response = client.post("/login", data={"username": "your_username", "password": "your_password"})

    assert response.status_code == 200  # Assuming successful login
    assert "access_token" in response.json()  # Ensure that an access token is present

    assert "token_type" in response.json() and response.json()["token_type"] == "bearer"
    assert "expires_in" in response.json() and isinstance(response.json()["expires_in"], int)

    token_payload = response.json().get("access_token_payload", {})
    assert "sub" in token_payload and token_payload["sub"] == "your_username"

    assert "content-type" in response.headers and response.headers["content-type"] == "application/json"

    assert "password" not in response.json()

    assert "x-response-time" in response.headers and float(response.headers["x-response-time"]) < 1.0
