import requests

user_data={
    "username":"frans",
    "password":"123"
}
response=requests.post('http://127.0.0.1:8000/user',json=user_data)

print(response.status_code)