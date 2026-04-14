"""
Author Pydantic schemas :
Separate schemas for Create / Update / Response.
"""

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

# CREATE
class AuthorCreate(BaseModel):
    """What the client sends when creating a new author."""
    name: str = Field(..., min_length=1, max_length=255, examples=["Naguib Mahfouz"])
    bio: Optional[str] = Field(None, examples=["Egyptian novelist and Nobel Prize winner."])

# UPDATE(PATCH)
class AuthorUpdate(BaseModel):
    """All fields are optional — client sends only what changed."""
    # In Update schema always Optional used
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    bio: Optional[str] = None

# RESPONSE (Read)
class AuthorResponse(BaseModel):
    """Returned to the client — includes the DB-generated id."""
    id: int
    name: str
    bio: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# RESPONSE with nested Books 
class BookBrief(BaseModel):
    """Minimal book info shown inside an author response."""
    id: int
    title: str
    price: float

    model_config = ConfigDict(from_attributes=True)


class AuthorWithBooksResponse(AuthorResponse):
    """Author + the list of their books (eager-loaded)."""
    books: list[BookBrief] = []