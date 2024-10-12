import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = sqlalchemy.orm.declarative_base()