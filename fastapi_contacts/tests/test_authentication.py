# fastapi_contacts/tests/test_authentication.py
from fastapi.testclient import TestClient
from fastapi_contacts.app.routes import router

client = TestClient(router)


def test_login_success():
    response = client.post("/login", json={"username": "test_user", "password": "test_password"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_failure():
    response = client.post("/login", json={"username": "invalid_user", "password": "invalid_password"})
    assert response.status_code == 401
    assert "detail" in response.json() and response.json()["detail"] == "Incorrect username or password"


def test_logout():

    login_response = client.post("/login", json={"username": "test_user", "password": "test_password"})
    access_token = login_response.json()["access_token"]

    logout_response = client.post("/logout", headers={"Authorization": f"Bearer {access_token}"})

    assert logout_response.status_code == 200
    assert "message" in logout_response.json() and logout_response.json()["message"] == "Logout successful"
