"""
Review Model:
Represents a reader's review for a specific book.
Relationship: Many Reviews → One Book  (Many-to-One)
"""

from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from core.database import Base


class Review(Base):
    __tablename__ = "reviews"

    # Columns 
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)   # 1-5 stars
    content = Column(Text, nullable=True)
    reviewer_name = Column(Text, nullable=True, default="Anonymous")

    # Foreign keys
    book_id = Column(
        Integer,
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Relationships
    book = relationship("Book", back_populates="reviews")

    def __repr__(self) -> str:
        return f"<Review(id={self.id}, rating={self.rating}, book_id={self.book_id})>"

