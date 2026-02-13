from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum

class DocumentStatus(str ,Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    INDEXED = "indexed"
    FAILED = "failed"


@dataclass
class Document:
    filename: str
    file_path: str
    file_size: int
    status : DocumentStatus = DocumentStatus.PENDING
    chunks_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    error_message: Optional[str] = None

@property
def is_indexed(self)-> bool:
    return self.status == DocumentStatus.INDEXED

@property
def size_human(self)-> str:
    if self.file_size < 1024:
        return f"{self.file_size} B"
    elif self.file_size < 1024**2:
        return f"{self.file_size / 1024:.1f} KB"
    return f"{self.file_size / 1024**2:.1f} MB"