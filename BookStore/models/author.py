"""
Author Model:
Represents a book author in the database.
Relationship: One Author → Many Books  (One-to-Many)
"""

from sqlalchemy import Column, Integer, String, Text 
from sqlalchemy.orm import relationship

from core.database import Base

class Author(Base):
    __tablename__ = "authors"

    # Columns
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    bio = Column(Text, nullable=True)

    # Relationships : 
    # An author can have many books.
    # cascade="all, delete-orphan" -> if author is deleted -> all their books are deleted automatically.
    books = relationship(
        "Book",
        back_populates="author",
        cascade="all, delete-orphan",
        lazy="selectin",  # eager-load books when querying authors
    )

    # determine how the object appear when we print it in the terminal
    def __repr__(self) -> str:
        return f"<Author(id={self.id}, name='{self.name}')>"