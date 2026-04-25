"""
API v1 Router:
collects all endpoint routers and groups
them under the /api/v1 prefix.
"""

from fastapi import APIRouter

from api.v1.endpoints import authors, books, reviews

api_router = APIRouter()

api_router.include_router(
    authors.router,
    prefix="/authors",
    tags=["📝 Authors"]
)

api_router.include_router(
    books.router,
    prefix="/books",
    tags=["📚 Books"],
)

api_router.include_router(
    reviews.router,
    prefix="/reviews",
    tags=["⭐ Reviews"],
)
