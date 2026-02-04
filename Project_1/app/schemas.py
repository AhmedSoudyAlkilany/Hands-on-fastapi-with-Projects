from enum import Enum
from pydantic import BaseModel, Field

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