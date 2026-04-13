"""
Database Engine & Session Management
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from core.config import settings

# Build the Engine
_connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite needs this flag so FastAPI threads can share
    # the same connection safely.
    _connect_args["check_same_thread"] = False

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=_connect_args,
    echo=True, # prints every SQL statement
)

# create the session
# Each API request will get its own "session" (a conversation with the database)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# Declaritive Base 
# Every model (Author, Book, Review) will inherit from this.
# It gives them the ability to describe SQL tables using plain Python classes.

class Base(DeclarativeBase):
    """SQLAlchemy 2.0+ style declarative base."""
    pass


# Dependency - get_db()
# FastAPI's "Dependency Injection" system will call this
# function automatically for every request that needs a DB
# session, and will close it when the request is done.

def get_db():
    """
    Yields a database session and ensures it is closed
    after the request finishes, even if an error occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()