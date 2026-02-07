from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from sqlalchemy.orm import selectinload

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
    async def create(db: AsyncSession, data: schemas.CategoryCreate) -> models.Category:
        return await CategoryCRUD.create_category(db, data)

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
    

class PromptCRUD:
    
    @staticmethod
    async def create(db: AsyncSession, data: schemas.PromptCreate) -> models.Prompt:
        prompt = models.Prompt(**data.model_dump())
        db.add(prompt)
        await db.flush()
        await db.refresh(prompt, ["category"])
        return prompt
    
    @staticmethod
    async def get_by_id(db: AsyncSession, id: int) -> Optional[models.Prompt]:
        result = await db.execute(
            select(models.Prompt)
            .options(selectinload(models.Prompt.category))
            .where(models.Prompt.id == id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all(
        db: AsyncSession,
        page: int = 1,
        per_page: int = 10
    ) -> schemas.PromptListResponse:
        # Count
        count_result = await db.execute(select(func.count(models.Prompt.id)))
        total = count_result.scalar() or 0
        
        # Query
        offset = (page - 1) * per_page
        result = await db.execute(
            select(models.Prompt)
            .options(selectinload(models.Prompt.category))
            .offset(offset)
            .limit(per_page)
            .order_by(models.Prompt.created_at.desc())
        )
        items = result.scalars().all()
        
        return schemas.PromptListResponse(
            items=items,
            total=total,
            page=page,
            pages=(total + per_page - 1) // per_page
        )
    
    @staticmethod
    async def update(
        db: AsyncSession,
        prompt: models.Prompt,
        data: schemas.PromptUpdate
    ) -> models.Prompt:
        update_data = data.model_dump(exclude_unset=True)
        for k, v in update_data.items():
            setattr(prompt, k, v)
        await db.flush()
        await db.refresh(prompt, ["category"])
        return prompt
    
    @staticmethod
    async def delete(db: AsyncSession, prompt: models.Prompt):
        await db.delete(prompt)
