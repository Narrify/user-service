"""
This module contains the db configuration and related operations.
"""

import os
import traceback

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

async def get_db():
    """
    Get the database session.
    """
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        # Imprimir el mensaje de error de forma detallada con traceback
        error_details = traceback.format_exc()
        print(f"Un error en obtener la sesion de la base de datos: {error_details}{e}")
    finally:
        try:
            db.close()
        except NameError:
            # Si 'db' no fue creado debido a un error, evitar un segundo error en el cierre
            print("La sesión no pudo ser cerrada porque no se estableció una conexión.")