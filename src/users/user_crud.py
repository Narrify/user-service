# user_crud.py

from fastapi import HTTPException
from passlib.context import CryptContext
from src.users.user_models import UserInDB

# Base de datos falsa para el ejemplo
fake_users_db = {}

# Configuración para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password for storing."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a stored password against one provided by user."""
    return pwd_context.verify(plain_password, hashed_password)


def get_user(username: str) -> UserInDB:
    """Get a user by username."""
    user = fake_users_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_user(username: str, password: str) -> UserInDB:
    """Create a new user."""
    if username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = hash_password(password)
    user = UserInDB(username=username, password=hashed_password)
    fake_users_db[username] = user  # Guarda el nuevo usuario en la "base de datos"
    return user
