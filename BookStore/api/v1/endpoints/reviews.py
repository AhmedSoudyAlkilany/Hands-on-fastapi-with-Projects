"""
Review Endpoints:
Full CRUD + filter-by-book + average-rating for the Review resource.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core.database import get_db
from crud import book_crud, review_crud
from schemas.review import ReviewCreate, ReviewResponse, ReviewUpdate

router = APIRouter()


# POST /reviews/
@router.post(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new review",
)
def create_review(
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
) -> Any:
    """
    Create a new review for a book.
    The **book_id** must reference an existing book.
    **rating** must be between 1 and 5.
    """
    if not book_crud.get(db=db, obj_id=review_in.book_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {review_in.book_id} not found",
        )
    return review_crud.create(db=db, obj_in=review_in)


# GET /reviews/by-book/{book_id}
@router.get(
    "/by-book/{book_id}",
    response_model=List[ReviewResponse],
    summary="Get reviews for a specific book",
)
def list_reviews_by_book(
    book_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """Retrieve all reviews for a given book."""
    if not book_crud.get(db=db, obj_id=book_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    return review_crud.get_reviews_by_book(db=db, book_id=book_id)


# GET /reviews/average/{book_id}
@router.get(
    "/average/{book_id}",
    summary="Get the average rating for a book",
)
def get_average_rating(
    book_id: int,
    db: Session = Depends(get_db),
) -> dict:
    """Calculate and return the average rating for a book."""
    if not book_crud.get(db=db, obj_id=book_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    avg = review_crud.get_average_rating(db=db, book_id=book_id)
    return {"book_id": book_id, "average_rating": avg}


# GET /reviews/{review_id}
@router.get(
    "/{review_id}",
    response_model=ReviewResponse,
    summary="Get a specific review",
)
def get_review(
    review_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """Retrieve a single review by its ID."""
    db_review = review_crud.get(db=db, obj_id=review_id)
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id {review_id} not found",
        )
    return db_review


# PATCH /reviews/{review_id}
@router.patch(
    "/{review_id}",
    response_model=ReviewResponse,
    summary="Update a review",
)
def update_review(
    review_id: int,
    review_in: ReviewUpdate,
    db: Session = Depends(get_db),
) -> Any:
    """Partially update a review."""
    db_review = review_crud.get(db=db, obj_id=review_id)
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id {review_id} not found",
        )
    return review_crud.update(db=db, db_obj=db_review, obj_in=review_in)


# DELETE /reviews/{review_id}
@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a review",
)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete a review."""
    db_review = review_crud.get(db=db, obj_id=review_id)
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id {review_id} not found",
        )
    review_crud.delete(db=db, obj_id=review_id)
