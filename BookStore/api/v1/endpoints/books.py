"""
Book Endpoints:
Full CRUD + search + filter-by-author for the Book resource.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core.database import get_db
from crud import author_crud, book_crud
from schemas.book import (
    BookCreate,
    BookResponse,
    BookUpdate,
    BookWithReviewsResponse,
)

router = APIRouter()


# POST /books/ 
@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new book",
)
def create_book(
    book_in: BookCreate,
    db: Session = Depends(get_db),
) -> Any:
    """
    Create a new book.
    The **author_id** must reference an existing author.
    """
    # Verify the author exists first
    if not author_crud.get(db=db, obj_id=book_in.author_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id {book_in.author_id} not found",
        )
    return book_crud.create(db=db, obj_in=book_in)


# GET /books/ 
@router.get(
    "/",
    response_model=List[BookResponse],
    summary="List all books",
)
def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> Any:
    """Retrieve a paginated list of books."""
    return book_crud.get_multi(db=db, skip=skip, limit=limit)


# GET /books/search?q=... 
@router.get(
    "/search",
    response_model=List[BookResponse],
    summary="Search books by title",
)
def search_books(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
) -> Any:
    """Search books whose title contains the query string."""
    return book_crud.search_by_title(db=db, query=q)


# GET /books/by-author/{author_id} 
@router.get(
    "/by-author/{author_id}",
    response_model=List[BookResponse],
    summary="Get all books by a specific author",
)
def list_books_by_author(
    author_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """Retrieve every book written by the given author."""
    if not author_crud.get(db=db, obj_id=author_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id {author_id} not found",
        )
    return book_crud.get_books_by_author(db=db, author_id=author_id)


# GET /books/{book_id} 
@router.get(
    "/{book_id}",
    response_model=BookWithReviewsResponse,
    summary="Get book details (with reviews)",
)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Retrieve a single book by ID.
    The response includes its reviews.
    """
    db_book = book_crud.get(db=db, obj_id=book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    return db_book


# PATCH /books/{book_id} 
@router.patch(
    "/{book_id}",
    response_model=BookResponse,
    summary="Update a book",
)
def update_book(
    book_id: int,
    book_in: BookUpdate,
    db: Session = Depends(get_db),
) -> Any:
    """Partially update a book's information."""
    db_book = book_crud.get(db=db, obj_id=book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    # If they're changing author_id, verify new author exists
    if book_in.author_id is not None:
        if not author_crud.get(db=db, obj_id=book_in.author_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Author with id {book_in.author_id} not found",
            )
    return book_crud.update(db=db, db_obj=db_book, obj_in=book_in)


# DELETE /books/{book_id}
@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a book",
)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete a book and all its reviews (cascade)."""
    db_book = book_crud.get(db=db, obj_id=book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    book_crud.delete(db=db, obj_id=book_id)
