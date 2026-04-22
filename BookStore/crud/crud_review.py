"""
CRUD operations specific to the Review model.
"""

from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.review import Review
from schemas.review import ReviewCreate, ReviewUpdate


class CRUDReview(CRUDBase[Review, ReviewCreate, ReviewUpdate]):
    def __init__(self):
        super().__init__(Review)

    def get_reviews_by_book(
        self, db: Session, *, book_id: int
    ) -> List[Review]:
        """Get all reviews for a specific book."""
        return db.query(Review).filter(Review.book_id == book_id).all()

    def get_average_rating(self, db: Session, *, book_id: int) -> float:
        """Calculate the average rating for a specific book."""
        result = (
            db.query(func.avg(Review.rating))
            .filter(Review.book_id == book_id)
            .scalar()
        )
        return round(result, 2) if result else 0.0
