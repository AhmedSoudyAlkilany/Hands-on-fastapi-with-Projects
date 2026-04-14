"""
Book Model:
Represents a book in the database.
Relationships:
    Many Books -> One Author   (Many-to-One via ForeignKey)
    One Book   -> Many Reviews (One-to-Many)
"""

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from core.database import Base

class Book(Base):
    __tablename__ = "books"

    # Columns
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False, default=0.0)
    pages = Column(Integer, nullable=True)
    isbn = Column(String(13), nullable=True, unique=True)

    # Foreign keys
    author_id = Column(
        Integer,
        ForeignKey("authors.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relationships
    author = relationship("Author", back_populates="books")
    reviews = relationship(
        "Review",
        back_populates="book",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    def __repr__(self) -> str:
        return f"<Book(id={self.id}, title='{self.title}')>"

