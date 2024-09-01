import os.path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.utils.config import config

# Get database configuration
db_name = config['database']['name']
db_path = config['database']['path']

# Construct full path to the database file
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ful_db_path = os.path.join(project_root, db_path, db_name)
SQLALCHEMY_DATABASE_URL = f"sqlite:///{ful_db_path}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()