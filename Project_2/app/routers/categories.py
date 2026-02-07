"""Category routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas import CategoryCreate, CategoryResponse
from app.crud import CategoryCRUD

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    return await CategoryCRUD.create(db, data)


@router.get("/", response_model=List[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await CategoryCRUD.get_all(db)


@router.get("/{id}", response_model=CategoryResponse)
async def get_category(id: int, db: AsyncSession = Depends(get_db)):
    cat = await CategoryCRUD.get_by_id(db, id)
    if not cat:
        raise HTTPException(404, "Not found")
    return cat
