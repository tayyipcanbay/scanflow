"""
Initialize database and create tables.
"""
from app.database.connection import Base, engine
from app.models import *  # noqa: F401, F403

if __name__ == "__main__":
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

