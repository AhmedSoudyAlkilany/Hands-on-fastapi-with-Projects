from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routers import categories, prompts

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize the database
    await init_db()
    print("Database initialized.")
    yield
    
app = FastAPI(title="Prompt Management API", lifespan=lifespan)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(categories.router, prefix="/api/v1")
app.include_router(prompts.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Prompt Manager", "docs": "/docs"}