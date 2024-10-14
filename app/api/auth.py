"This module contains the routes for the authentication of the user."
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.auth import create_access_token, verify_password
from app.crud.user_crud import get_user_by_username
from app.db.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)): # pylint: disable=line-too-long
    "Login for access token."
    user = get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user_id=user.id, username=user.username, role=user.role)
    return {"access_token": access_token, "token_type": "bearer"}
