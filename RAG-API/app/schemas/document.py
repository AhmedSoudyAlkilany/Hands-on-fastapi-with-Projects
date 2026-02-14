from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DocumentUploadResponse(BaseModel):
    """الرد بعد رفع مستند."""
    status: str = Field(..., description="حالة المعالجة")
    filename: str = Field(..., description="اسم الملف الأصلي")
    file_size: str = Field(..., description="حجم الملف (المقروء)")
    chunks_created: int = Field(..., description="عدد القطع المُنشأة")
    message: str = Field(..., description="رسالة الحالة")


class DocumentInfo(BaseModel):
    """معلومات عن مستند واحد."""
    filename: str
    size_bytes: int
    size_human: str
    status: str
    chunks_count: int
    created_at: Optional[datetime] = None


class DocumentListResponse(BaseModel):
    """رد قائمة المستندات."""
    total_documents: int
    total_chunks: int
    documents: List[DocumentInfo]


class DocumentDeleteResponse(BaseModel):
    """الرد بعد حذف مستند."""
    status: str = "deleted"
    filename: str
    chunks_deleted: int
