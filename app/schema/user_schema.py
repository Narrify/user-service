"""
Schema for user data
"""

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """
    User create schema class.
    """

    username: str
    email: EmailStr
    password: str
    role: str


class UserResponse(BaseModel):
    """
    User response schema class.
    """

    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        """
        ORM mode
        """

        # pylint: disable=too-few-public-methods

        orm_mode = True


class UserUpdate(BaseModel):
    """
    User update schema class.
    """

    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: str | None = None
