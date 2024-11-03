"""
This module contains the authentication configuration and related operations.
"""

from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.user_crud import get_user # pylint: disable=cyclic-import
from app.db.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenData(BaseModel):
    """
    Token data class.
    """

    username: str | None = None
    user_id: int | None = None
    role: str | None = None


def hash_password(password: str) -> str:
    """
    Hash the given password.
    """

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify the given password with the hashed password
    """

    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int, username: str, role: str):
    """
    Create an access token with the given data.
    """

    to_encode = {"sub": username, "user_id": user_id, "role": role}
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


def verify_token(token: str, credentials_exception):
    """
    Verify token and return the token data.
    """

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        role: str = payload.get("role")

        if username is None or user_id is None or role is None:
            raise credentials_exception

        token_data = TokenData(username=username, user_id=user_id, role=role)

        return token_data
    except JWTError as exc:
        raise credentials_exception from exc


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Get the current user from the token.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token, credentials_exception)
    user = get_user(db, user_id=token_data.user_id)

    if user is None:
        raise credentials_exception
    return user


def get_current_user_with_role(required_role: str):
    """
            Get the current user with the required role from the token.
            """
    def role_dependency(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """
        Get the current user with the required role from the token.
        """
        user = get_current_user(token, db)
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user
    return role_dependency
