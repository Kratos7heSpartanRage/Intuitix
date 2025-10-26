import os
from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv

load_dotenv()

# Correct: Get the variable by its name "DATABASE_URL"
DATABASE_URL = os.getenv("DATABASE_URL") 

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
