"""
Generic CRUD Base Class : (create, read, update, delete)

"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.orm import Session

from core.database import Base

# Type variables — placeholders that get filled per-model
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class with default CRUD operations.
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model

    # READ one
    def get(self, db: Session, *, obj_id: int) -> Optional[ModelType]:
        """Get a single record by primary key."""
        return db.query(self.model).filter(self.model.id == obj_id).first()
    # READ many
    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ModelType]:
        """Get a paginated list of records."""
        return (
            db.query(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    # CREATE
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Insert a new record."""
        obj_data = obj_in.model_dump()           # Pydantic v2
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    # UPDATE
    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        """Update an existing record (partial update / PATCH)."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    # DELETE
    def delete(self, db: Session, *, obj_id: int) -> Optional[ModelType]:
        """Delete a record by primary key. Returns the deleted object."""
        obj = db.query(self.model).get(obj_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
    
    # COUNT
    def count(self, db: Session) -> int:
        """Return total number of records."""
        return db.query(self.model).count()