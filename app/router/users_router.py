"""
Users router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.user_crud import (create_user, get_user, get_user_by_username, get_users,
                                update_user, delete_user)
from app.db.database import get_db
from app.core.auth import get_current_user_with_role, get_current_user, oauth2_scheme
from app.schema.user_schema import UserCreate, UserUpdate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

def role_dependency(required_role: str):
    def wrapper(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        return get_current_user_with_role(required_role, token, db)
    return Depends(wrapper)

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: UserResponse = Depends(get_current_user)
):
    "Get current user"
    return current_user

@router.get("/", response_model=list[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user_with_role("admin"))
):
    """
    Get all users - Admin only.
    """
    
    users = get_users(db, skip=skip, limit=limit)

    return users


@router.post("/", response_model=UserResponse)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """

    db_user = get_user_by_username(db, username=user.username)

    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    return create_user(db, user=user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_existing_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user_with_role("admin"))
):
    """
    Update a user.
    """
    
    db_user = get_user(db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return update_user(db, db_user=db_user, user_update=user_update)


@router.delete("/{user_id}", response_model=UserResponse)
async def delete_existing_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user_with_role("admin"))
):
    """
    Delete a user - Admin only.
    """
    
    db_user = delete_user(db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user

"""
@router.post("/generate_story")
async def generate_story_endpoint(
    title: str,
    settings: dict,
    characters: list,
    plots: int = 1,
    endings: int = 1,
    current_user: UserResponse = Depends(get_current_user)
):
   
    story_instance = Story(title=title, settings=settings, characters=characters, plots=plots, endings=endings)
    response = story_instance.generate_story()
    
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    
    return response

@router.post("/generate_dialogue")
async def generate_dialogue_endpoint(
    story: str,
    settings: dict,
    characters: list,
    current_user: UserResponse = Depends(get_current_user)
):
    
    dialogue_instance = Dialogue(story=story, settings=settings, characters=characters)
    response = dialogue_instance.generate_dialogue()
    
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    
    return response

""" 