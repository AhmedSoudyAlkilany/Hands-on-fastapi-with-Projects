"""
Review Schemas 
"""

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


# CREATE 
class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5, examples=[4])
    content: Optional[str] = Field(None, examples=["A masterpiece of Arabic literature."])
    reviewer_name: Optional[str] = Field("Anonymous", examples=["Ahmed"])
    book_id: int = Field(..., gt=0, examples=[1])


# UPDATE 
class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    content: Optional[str] = None
    reviewer_name: Optional[str] = None


# RESPONSE (Read)
class ReviewResponse(BaseModel):
    id: int
    rating: int
    content: Optional[str] = None
    reviewer_name: Optional[str] = None
    book_id: int

    model_config = ConfigDict(from_attributes=True)
