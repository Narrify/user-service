from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_create_user():
    """
    crear usuarios
    """
    # ARRANGE
    json_body = {
        "username": "frans12345",
        "password": "frans",
        "email": "fransqwerty@gmail.com"
    }

    # ACT
    response = client.post("/users", json=json_body)

    # ASSERT
    assert response.status_code in (
        201, 200), "create user not return 200 status code"