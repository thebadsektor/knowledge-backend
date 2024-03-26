from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from databases import Database

# Configure the database URL
DATABASE_URL = "sqlite:///./test.db"
Base = declarative_base()


# Create the database engine and connect to it
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Create the database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the FastAPI database instance
database = Database(DATABASE_URL)