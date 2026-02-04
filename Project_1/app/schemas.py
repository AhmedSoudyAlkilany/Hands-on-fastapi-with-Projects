from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List

class SentimentType(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class LanguageCode(str, Enum):
    ARABIC = "ar"
    ENGLISH = "en"
    FRENCH = "fr"
    UNKNOWN = "unknown"

class SentimentResult(BaseModel):
    type : SentimentType
    score : float = Field(..., ge=-1.0, le=1.0)
    confidence : float = Field(..., ge=0.0, le=1.0)

class TextAnalysisRequest(BaseModel):
    text : str = Field(..., min_length=10, max_length=10000)
    include_keywords: bool = Field(default=True)
    include_summary:bool = Field(default=False)
    max_keywords: int = Field(default=5, ge=1, le=20)


class TextAnalysisResponse(BaseModel):
    original_text: str
    language: LanguageCode
    word_count: int
    chatacter_count: int
    sentiment: SentimentResult
    keywords: Optional[List[str]] = None
    summary: Optional[str] = None
    processing_time_ms: float