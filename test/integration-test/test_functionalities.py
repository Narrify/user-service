from fastapi.testclient import TestClient
from app.main import app
import random
import string

client = TestClient(app)

username_random = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
password_random = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
email_random = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
email_random= email_random + "@gmail.com"



def test_create_user():
    #ARRANGE
    json_body = {
        "username": username_random,
        "password": password_random,
        "email": email_random
    }

    #ACT
    response = client.post("/users",json=json_body)

    #ASSERT
    assert response.status_code == 201 or response.status_code == 200, "create user not return 200 status code"


def test_login_user():
    #ARRANGE - login-user-no-admin
    data={"username":username_random, "password":password_random}

    #ACT
    response = client.post("/auth/token", data=data)

    #ASSERT
    assert response.status_code == 200, "Token not received, login unsuccessful"
    assert response.json()["token_type"] == "bearer", "Token not received"




