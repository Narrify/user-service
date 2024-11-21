"""
This module contains the db configuration and related operations.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
    """
    Get the database session.
    """
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        print(f"Un error en obtener la sesion de la base de datos, {e}")    
    finally:
        db.close()
