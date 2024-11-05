"""
User CRUD
"""

from sqlalchemy.orm import Session

from app.models.user import User
from app.schema.user_schema import UserCreate, UserUpdate


def create_user(db: Session, user: UserCreate):
    """
    Create a new user.
    """
    from app.core.auth import hash_password

    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
        role="user",
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user(db: Session, user_id: int):
    """
    Get a user by id.
    """

    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    """
    Get a user by username.
    """

    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    """
    Get all users.
    """

    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, db_user: User, user_update: UserUpdate):
    """
    Update a user.
    """

    for field, value in user_update.model_dump(exclude_unset=True).items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, user_id: int):
    """
    Delete a user.
    """

    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user:
        db.delete(db_user)
        db.commit()

    return db_user
