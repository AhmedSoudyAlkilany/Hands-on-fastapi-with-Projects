"""
CRUD operations specific to the Book model.
"""

from typing import List

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.book import Book
from schemas.book import BookCreate, BookUpdate


class CRUDBook(CRUDBase[Book, BookCreate, BookUpdate]):
    def __init__(self):
        super().__init__(Book)

    def get_books_by_author(
        self, db: Session, *, author_id: int
    ) -> List[Book]:
        """Get all books written by a specific author."""
        return db.query(Book).filter(Book.author_id == author_id).all()

    def search_by_title(
        self, db: Session, *, query: str
    ) -> List[Book]:
        """Search books whose title contains the query string."""
        return (
            db.query(Book)
            .filter(Book.title.ilike(f"%{query}%"))
            .all()
        )
