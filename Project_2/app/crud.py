from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app import models, schemas

class CategoryCRUD:
    @staticmethod
    async def create_category(db: AsyncSession, data: schemas.CategoryCreate) -> models.Category:
        category = models.Category(**data.model_dump())
        db.add(category)
        await db.flush()
        await db.refresh(category)
        return category

    @staticmethod
    async def get_all(db: AsyncSession) -> List[models.Category]:
        result = await db.execute(select(models.Category))
        return result.scalars().all()
    
    @staticmethod
    async def get_by_id(db: AsyncSession, id: int) -> Optional[models.Category]:
        result = await db.execute(
            select(models.Category).where(models.Category.id == id)
        )
        return result.scalar_one_or_none()