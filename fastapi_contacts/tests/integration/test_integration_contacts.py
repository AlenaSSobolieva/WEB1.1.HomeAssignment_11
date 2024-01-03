# fastapi_contacts/tests/integration/test_integration_contacts.py
from fastapi.testclient import TestClient
from fastapi_contacts.main import app

client = TestClient(app)


def test_integration_create_contact():
    # Test creating a contact
    contact_data = {
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com",
        "phone_number": "123456789",
        "birthday": "1990-01-01",
        "additional_info": "Some additional information"
    }

    response = client.post("/contacts/", json=contact_data)

    assert response.status_code == 201  # 201 Created
    assert "id" in response.json()  # Ensure that the response contains the contact ID
    assert response.json()["name"] == "John"
    assert response.json()["email"] == "john.doe@example.com"
    assert response.json()["phone_number"] == "123456789"
    assert response.json()["birthday"] == "1990-01-01"
    assert response.json()["additional_info"] == "Some additional information"


def test_integration_get_contact_by_id():
    # First, create a contact to retrieve later
    contact_data = {
        "name": "Jane",
        "surname": "Doe",
        "email": "jane.doe@example.com",
        "phone_number": "987654321",
        "birthday": "1985-05-05",
        "additional_info": "Some additional information"
    }

    create_response = client.post("/contacts/", json=contact_data)
    created_contact_id = create_response.json()["id"]

    # Test retrieving the contact by ID
    response = client.get(f"/contacts/{created_contact_id}")

    assert response.status_code == 200  # 200 OK
    assert response.json()["id"] == created_contact_id
    assert response.json()["name"] == "Jane"
    assert response.json()["surname"] == "Doe"
    assert response.json()["email"] == "jane.doe@example.com"
    assert response.json()["phone_number"] == "987654321"
    assert response.json()["birthday"] == "1985-05-05"
    assert response.json()["additional_info"] == "Some additional information"

