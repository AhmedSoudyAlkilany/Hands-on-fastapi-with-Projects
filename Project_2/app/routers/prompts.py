"""Prompt routes"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import PromptCreate, PromptUpdate, PromptResponse, PromptListResponse
from app.crud import PromptCRUD

router = APIRouter(prefix="/prompts", tags=["Prompts"])


@router.post("/", response_model=PromptResponse, status_code=201)
async def create_prompt(data: PromptCreate, db: AsyncSession = Depends(get_db)):
    return await PromptCRUD.create(db, data)


@router.get("/", response_model=PromptListResponse)
async def get_prompts(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await PromptCRUD.get_all(db, page, per_page)


@router.get("/{id}", response_model=PromptResponse)
async def get_prompt(id: int, db: AsyncSession = Depends(get_db)):
    prompt = await PromptCRUD.get_by_id(db, id)
    if not prompt:
        raise HTTPException(404, "Not found")
    return prompt


@router.put("/{id}", response_model=PromptResponse)
async def update_prompt(
    id: int,
    data: PromptUpdate,
    db: AsyncSession = Depends(get_db)
):
    prompt = await PromptCRUD.get_by_id(db, id)
    if not prompt:
        raise HTTPException(404, "Not found")
    return await PromptCRUD.update(db, prompt, data)


@router.delete("/{id}", status_code=204)
async def delete_prompt(id: int, db: AsyncSession = Depends(get_db)):
    prompt = await PromptCRUD.get_by_id(db, id)
    if not prompt:
        raise HTTPException(404, "Not found")
    await PromptCRUD.delete(db, prompt)