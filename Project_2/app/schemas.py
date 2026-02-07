"start with Category schemas"
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str]= None


class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PromptBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    content: str = Field(..., min_length=10)
    category_id: Optional[int] = None

class PromptCreate(PromptBase):
    pass

class PromptUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None
    is_favorite: Optional[bool] = None


class PromptResponse(PromptBase):
    id: int
    rating: Optional[float] = None
    usage_count: int
    is_favorite: bool
    created_at: datetime
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True

class PromptListResponse(BaseModel):
    items: list[PromptResponse]
    total: int
    page: int
    pages: int
   
