from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_create_user():
    """
    crear usuarios
    """
    # ARRANGE
    json_body = {
        "username": "fransds12345qwerty",
        "password": "fransqwerty",
        "email": "fransnarrifyqwerty@gmail.com"
    }

    # ACT
    try:
        response = client.post("/users", json=json_body)
    except Exception as e:
        print(f"error creando usuario{e}")
    # ASSERT
    assert response.status_code in (
        201, 200), "create user not return 200 status code"
