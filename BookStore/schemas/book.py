"""
Book schemas
"""

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

# CREATE
class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, examples=["Palace Walk"])
    description: Optional[str] = Field(None, examples=["A sweeping family saga..."])
    price: float = Field(..., gt=0, examples=[29.99])
    pages: Optional[int] = Field(None, gt=0, examples=[512])
    isbn: Optional[str] = Field(None, pattern=r"^\d{10,13}$", examples=["9780385264662"])
    author_id: int = Field(..., gt=0, examples=[1])

# UPDATE 
class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    pages: Optional[int] = Field(None, gt=0)
    isbn: Optional[str] = Field(None, pattern=r"^\d{10,13}$") # ISBN = International Standard Book Number
    author_id: Optional[int] = Field(None, gt=0)

# RESPONSE (Read)
class BookResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    price: float
    pages: Optional[int] = None
    isbn: Optional[str] = None
    author_id: int

    model_config = ConfigDict(from_attributes=True)

# RESPONSE with nested Reviews
class ReviewBrief(BaseModel):
    id: int
    rating: int
    content: Optional[str] = None
    reviewer_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class BookWithReviewsResponse(BookResponse):
    reviews: list[ReviewBrief] = []