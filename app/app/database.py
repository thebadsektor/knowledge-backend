from sqlalchemy import create_engine, Column, String, Float, Boolean, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from databases import Database

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

def create_database():
    Base.metadata.create_all(bind=engine)

def get_session():
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session()

database = Database(DATABASE_URL)