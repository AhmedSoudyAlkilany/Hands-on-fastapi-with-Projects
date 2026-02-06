from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from app.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
)

Base = declarative_base()

async def init_db():
    "Initialize the database by creating all tables."
    async with engine.begin() as conn:
        from app import models
        await conn.run_sync(Base.metadata.create_all)
