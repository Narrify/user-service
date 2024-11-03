"""
test de seguridad
"""
import random
import string
from http.client import HTTPException

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)
"""
test client, test en fastapi
"""

USERNAME_RANDOM = ''.join(
    random.choices(
        string.ascii_letters +
        string.digits,
        k=5))
PASSWORD_RANDOM = ''.join(
    random.choices(
        string.ascii_letters +
        string.digits,
        k=5))
EMAIL_RANDOM = ''.join(
    random.choices(
        string.ascii_letters +
        string.digits,
        k=5))
EMAIL_RANDOM = EMAIL_RANDOM + "@gmail.com"

json_body = {
    "username": USERNAME_RANDOM,
    "password": PASSWORD_RANDOM,
    "email": EMAIL_RANDOM
}

try:
    response_create = client.post("/users", json=json_body)
    data = {"username": USERNAME_RANDOM, "password": PASSWORD_RANDOM}
    response_login = client.post("/auth/token", data=data)
except HTTPException as e:
    print(f"error on create user or login user for testing purposes: {e}")


def test_endpoints_admin_only():
    """
    testing endpoints admin
    """
    # arrange
    data_login = {"username": USERNAME_RANDOM, "password": PASSWORD_RANDOM}
    response = client.post("/auth/token", data=data_login)
    token = response.json()["access_token"]
    headers = {"Authorization": "Bearer " + token}

    # act
    response_get_user = client.get("/users", headers=headers)
    response_get_user_id = client.get("/users/2", headers=headers)
    response_put_user = client.put("/users/2", headers=headers)
    response_delete_user = client.delete("/users/2", headers=headers)

    # assert
    assert response_get_user.status_code in (
        401, 403), "no-admin user gets users list"
    assert response_get_user_id.status_code in (
        401, 403, 405), "no-admin user see details of other users"
    assert response_put_user.status_code in (
        401, 403), "no-admin user updates user's info"
    assert response_delete_user.status_code in (
        401, 403), "no-admin user deletes users"


def test_endpoints_non_admin_only():
    """
    testing endpoints non-admin
    """
    # arrange
    data_na = {"username": USERNAME_RANDOM, "password": PASSWORD_RANDOM}
    response = client.post("/auth/token", data=data_na)
    token = response.json()["access_token"]
    headers = {"Authorization": "Bearer " + token}

    # act
    response = client.get("users/me", headers=headers)

    # assert
    assert response.status_code == 200, "no-admin endpoint refuses user role"


def test_create_user_same_username():
    # arrange
    """
    crear un usuario con el mismo username
    """
    json_create_user = {
        "username": USERNAME_RANDOM,
        "password": PASSWORD_RANDOM + "test",
        "email": EMAIL_RANDOM + "m"
    }

    # act
    response = client.post("/users", json=json_create_user)

    # assert
    assert response.status_code in (
        400, 403), "API allow create users with same username"


def test_sql_injection_login():
    """
    SQL Injection
    """
    # arrange
    data_sql = {
        "username": USERNAME_RANDOM,
        "password": f"{PASSWORD_RANDOM}' OR '1'=='1"
    }

    # act
    response = client.post("/auth/token", data=data_sql)

    # assert
    assert response.status_code in (
        400, 401, 403), "SQL Injection exploit detected"
