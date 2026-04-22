"""
CRUD operations specific to the Author model, 
Inherits all gerneric operations from CRUDBase 
and adds author-specific queries.
"""
from typing import List, Optional

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.author import Author
from schemas.author import AuthorCreate, AuthorUpdate


class CRUDAuthor(CRUDBase[Author, AuthorCreate, AuthorUpdate]):
    def __init__(self):
        super().__init__(Author)

    def get_by_name(self, db: Session, *, name: str) -> Optional[Author]:
        """Find an author by exact name match."""
        return db.query(Author).filter(Author.name == name).first()

    def search_by_name(self, db: Session, *, query: str) -> List[Author]:
        """Search authors whose name contains the query string."""
        return (
            db.query(Author)
            .filter(Author.name.ilike(f"%{query}%"))
            .all()
        )