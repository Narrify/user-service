# user_handlers.py

from fastapi import APIRouter, Depends
from users.user_crud import create_user, get_user
from users.user_models import UserInDB

router = APIRouter()

@router.post("/users/", response_model=UserInDB)
async def register_user(username: str, password: str):
    return create_user(username=username, password=password)

@router.get("/users/{username}", response_model=UserInDB)
async def read_user(username: str):
    return get_user(username=username)
