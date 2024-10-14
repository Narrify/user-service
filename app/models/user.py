"This module contains the User model class."
from sqlalchemy import Column, Integer, String
from app.db.database import Base

class User(Base):
    "This class represents the user table in the database."
    # pylint: disable=too-few-public-methods
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
