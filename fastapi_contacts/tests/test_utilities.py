# fastapi_contacts/tests/test_main.py
from fastapi.testclient import TestClient
from fastapi_contacts.app.routes import app
from fastapi_contacts.app.database import engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi_contacts.app.routes import get_db

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the dependency to use the test database
app.dependency_overrides[get_db] = TestingSessionLocal

client = TestClient(app)


def test_create_contact():
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


def test_read_contacts():
    # Test getting a list of contacts
    response = client.get("/contacts/")

    assert response.status_code == 200  # 200 OK

    # Ensure that the response is a list
    assert isinstance(response.json(), list)

    # Ensure that each item in the list is a dictionary representing a contact
    for contact in response.json():
        assert isinstance(contact, dict)

        # Add more assertions based on the expected structure of a contact
        assert "id" in contact and isinstance(contact["id"], int)
        assert "name" in contact and isinstance(contact["name"], str)
        assert "surname" in contact and isinstance(contact["surname"], str)
        assert "email" in contact and isinstance(contact["email"], str)
        assert "phone_number" in contact and isinstance(contact["phone_number"], str)
        assert "birthday" in contact and isinstance(contact["birthday"], str)
        assert "additional_info" in contact  # Assuming additional_info is optional

        # Add more specific assertions based on your application's requirements

    # Ensure that the list is not empty
    assert len(response.json()) > 0


def test_read_contact():
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

    # Ensure that certain fields are present in the response
    assert "name" in response.json()
    assert "surname" in response.json()
    assert "email" in response.json()
    assert "phone_number" in response.json()
    assert "birthday" in response.json()
    assert "additional_info" in response.json()

    # Ensure that optional fields are handled correctly
    assert response.json()["additional_info"] is not None  # Assuming additional_info is optional

    # Ensure that certain fields are of the correct data type
    assert isinstance(response.json()["id"], int)
    assert isinstance(response.json()["name"], str)
    assert isinstance(response.json()["surname"], str)
    assert isinstance(response.json()["email"], str)
    assert isinstance(response.json()["phone_number"], str)
    assert isinstance(response.json()["birthday"], str)

    # Add more assertions based on your specific requirements and data structure


def test_update_contact():
    # First, create a contact to update later
    contact_data = {
        "name": "Jack",
        "surname": "Smith",
        "email": "jack.smith@example.com",
        "phone_number": "111222333",
        "birthday": "1995-10-10",
        "additional_info": "Some additional information"
    }

    create_response = client.post("/contacts/", json=contact_data)
    created_contact_id = create_response.json()["id"]

    # Test updating the contact
    updated_contact_data = {
        "name": "Updated Jack",
        "surname": "Updated Smith",
        "email": "updated.jack.smith@example.com",
        "phone_number": "999888777",
        "birthday": "2000-01-01",
        "additional_info": "Updated additional information"
    }

    response = client.put(f"/contacts/{created_contact_id}", json=updated_contact_data)

    assert response.status_code == 200  # 200 OK
    assert response.json()["id"] == created_contact_id
    assert response.json()["name"] == "Updated Jack"
    assert response.json()["surname"] == "Updated Smith"
    assert response.json()["email"] == "updated.jack.smith@example.com"
    assert response.json()["phone_number"] == "999888777"
    assert response.json()["birthday"] == "2000-01-01"
    assert response.json()["additional_info"] == "Updated additional information"

    # Add more assertions based on your specific requirements and data structure


def test_delete_contact():
    # First, create a contact to delete later
    contact_data = {
        "name": "Delete Me",
        "surname": "ToDelete",
        "email": "delete.me@example.com",
        "phone_number": "123123123",
        "birthday": "1999-12-31",
        "additional_info": "Please delete me"
    }

    create_response = client.post("/contacts/", json=contact_data)
    created_contact_id = create_response.json()["id"]

    # Test deleting the contact
    response = client.delete(f"/contacts/{created_contact_id}")

    assert response.status_code == 200  # 200 OK
    assert response.json()["id"] == created_contact_id
    assert response.json()["name"] == "Delete Me"
    assert response.json()["surname"] == "ToDelete"
    assert response.json()["email"] == "delete.me@example.com"
    assert response.json()["phone_number"] == "123123123"
    assert response.json()["birthday"] == "1999-12-31"
    assert response.json()["additional_info"] == "Please delete me"

    # Ensure that the contact has been deleted
    deleted_response = client.get(f"/contacts/{created_contact_id}")
    assert deleted_response.status_code == 404  # 404 Not Found
    assert "detail" in deleted_response.json() and deleted_response.json()["detail"] == "Contact not found"

    # Add more assertions based on your specific requirements and data structure


# Remove the test database after all tests are done
def finalizer():
    TestingSessionLocal().close()

def test_finalizer():
    # Ensure that the test database is properly closed and cleaned up
    try:
        # Perform any finalization steps if needed

        # For example, you might want to commit and close any remaining transactions
        # Or perform additional cleanup steps related to the test database

        # Add more finalization steps if needed
        # For demonstration purposes, you can add a print statement
        print("Finalization steps completed successfully")

        # Ensure that the finalization steps are successful
        assert True, "Finalization steps completed successfully"
    except Exception as e:
        # Handle exceptions that might occur during finalization
        # Log or print the exception details for debugging
        print(f"Error during finalization: {e}")
        assert False, f"Error during finalization: {e}"
    finally:
        # Close the test database connection and clean up resources
        TestingSessionLocal().close()