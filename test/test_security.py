from fastapi.testclient import TestClient
from app.main import app
import random
import string

client = TestClient(app)

username_random = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
password_random = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
email_random = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
email_random= email_random + "@gmail.com"

json_body = {
        "username": username_random,
        "password": password_random,
        "email": email_random
    }

try:
    response_create = client.post("/users",json=json_body)
    data={"username":username_random, "password":password_random}
    response_login = client.post("/auth/token", data=data)
except Exception as e:
    print(f"error on create user or login user for testing purposes: {e}")


def test_endpoints_admin_only():

    #arrange
    data = {"username": username_random, "password": password_random}
    response = client.post("/auth/token", data=data)
    token = response.json()["access_token"]
    headers = {"Authorization": "Bearer " + token}

    #act
    response_get_user = client.get("/users", headers=headers)
    response_get_user_id = client.get("/users/2", headers=headers)
    response_put_user = client.put("/users/2", headers=headers)
    response_delete_user = client.delete("/users/2", headers=headers)

    #assert
    assert response_get_user.status_code in (401, 403) , "no-admin user gets users list"
    assert response_get_user_id.status_code in (401, 403, 405), "no-admin user see details of other users"
    assert response_put_user.status_code in (401, 403), "no-admin user updates user's info"
    assert response_delete_user.status_code in (401, 403), "no-admin user deletes users"

def test_endpoints_non_admin_only():
    # arrange
    data = {"username": username_random, "password": password_random}
    response = client.post("/auth/token", data=data)
    token = response.json()["access_token"]
    headers = {"Authorization": "Bearer " + token}

    #act
    response = client.get("users/me", headers=headers)

    #assert
    assert response.status_code == 200, "no-admin endpoint refuses user role"



def test_create_user_same_username():
    #arrange

    json_body = {
        "username": username_random,
        "password": password_random+"test",
        "email" : email_random+"m"
    }

    #act
    response = client.post("/users",json=json_body)

    #assert
    assert response.status_code in (400,403), "API allow create users with same username"

def test_SQL_Injection_login():
    # arrange

    data = {
        "username": username_random,
        "password": f"{password_random}' OR '1'=='1"
    }

    # act
    response = client.post("/auth/token", data=data)

    # assert
    assert response.status_code in (400,401, 403), "SQL Injection exploit detected"

