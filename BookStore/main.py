"""
Books Store : Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.database import engine
from models import Base
from api.v1.router import api_router

# create Tables
Base.metadata.create_all(bind=engine)

# Intialize the app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# Root Health-check
@app.get("/", tags=["🏠 Root"])
def root():
    """
    Simple health-check endpoint
    """
    return{
       "status": "running",
        "project": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "docs": "/docs", 
    }