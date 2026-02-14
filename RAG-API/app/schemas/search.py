from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class SearchRequest(BaseModel):
    """طلب بحث بكل الخيارات."""
    query: str = Field(..., min_length=1, description="نص البحث")
    top_k: int = Field(default=5, ge=1, le=20, description="عدد النتائج")
    min_score: float = Field(default=0.3, ge=0, le=1, description="حد أدنى للتشابه")
    filter_source: Optional[str] = Field(None, description="تصفية حسب المستند")
    hybrid: bool = Field(default=True, description="بحث هجين (vector + كلمات)")


class SearchResultItem(BaseModel):
    """نتيجة بحث واحدة."""
    content: str
    source: str
    score: float
    metadata: Dict[str, Any]


class SimilarResult(BaseModel):
    """نتيجة بحث تشابه سريع."""
    content: str
    similarity: float
    source: str
