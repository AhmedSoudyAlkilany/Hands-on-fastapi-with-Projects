"""
Author Endpoints:
Full CRUD + search for the Author resource.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core.database import get_db
from crud import author_crud
from schemas.author import (
    AuthorCreate,
    AuthorResponse,
    AuthorUpdate,
    AuthorWithBooksResponse,
)

router = APIRouter()


# POST /authors/ 
@router.post(
    "/",
    response_model=AuthorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new author",
)
def create_author(
    author_in: AuthorCreate,
    db: Session = Depends(get_db),
) -> Any:
    """
    Create a new author record.
    - **name**: required — the author's full name
    - **bio**: optional — a short biography
    """
    return author_crud.create(db=db, obj_in=author_in)


# GET /authors/ 
@router.get(
    "/",
    response_model=List[AuthorResponse],
    summary="List all authors",
)
def list_authors(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Max records to return"),
    db: Session = Depends(get_db),
) -> Any:
    """Retrieve a paginated list of authors."""
    return author_crud.get_multi(db=db, skip=skip, limit=limit)


# GET /authors/search?q=... 
@router.get(
    "/search",
    response_model=List[AuthorResponse],
    summary="Search authors by name",
)
def search_authors(
    q: str = Query(..., min_length=1, description="Search query"),
    db: Session = Depends(get_db),
) -> Any:
    """Search authors whose name contains the query string."""
    return author_crud.search_by_name(db=db, query=q)


# GET /authors/{author_id}
@router.get(
    "/{author_id}",
    response_model=AuthorWithBooksResponse,
    summary="Get author details (with books)",
)
def get_author(
    author_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Retrieve a single author by ID.
    The response includes their list of books.
    """
    db_author = author_crud.get(db=db, obj_id=author_id)
    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id {author_id} not found",
        )
    return db_author


# PATCH /authors/{author_id}
@router.patch(
    "/{author_id}",
    response_model=AuthorResponse,
    summary="Update an author",
)
def update_author(
    author_id: int,
    author_in: AuthorUpdate,
    db: Session = Depends(get_db),
) -> Any:
    """Partially update an author's information."""
    db_author = author_crud.get(db=db, obj_id=author_id)
    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id {author_id} not found",
        )
    return author_crud.update(db=db, db_obj=db_author, obj_in=author_in)


#  DELETE /authors/{author_id} 
@router.delete(
    "/{author_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an author",
)
def delete_author(
    author_id: int,
    db: Session = Depends(get_db),
) -> None:
    """
    Delete an author and all their books (cascade).
    Returns 204 No Content on success.
    """
    db_author = author_crud.get(db=db, obj_id=author_id)
    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id {author_id} not found",
        )
    author_crud.delete(db=db, obj_id=author_id)
