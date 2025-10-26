from sqlmodel import SQLModel
from database import engine  # Imports the engine from your existing database.py
import models # By importing models, SQLModel knows about your tables

def reset_database():
    """
    This script will drop all tables and recreate them from scratch
    based on your current models.py file.
    """
    print("ATTENTION: This will delete ALL existing data in your tables.")
    print("This action cannot be undone.")
    
    confirm = input("Type 'YES' to confirm and reset the database: ")
    
    if confirm == "YES":
        print("\nDropping all tables...")
        # We must import all models (like ReviewResult, Submission) in 'models.py'
        # so that SQLModel.metadata knows about them.
        SQLModel.metadata.drop_all(engine)
        print("All tables dropped.")
        
        print("\nCreating all tables...")
        SQLModel.metadata.create_all(engine)
        print("All tables created successfully based on your models.py.")
        print("Database is now in sync!")
    else:
        print("\nOperation aborted.")

if __name__ == "__main__":
    # This makes the script runnable from the command line
    reset_database()
