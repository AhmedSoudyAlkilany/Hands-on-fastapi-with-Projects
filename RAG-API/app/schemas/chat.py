from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class ChatRequest(BaseModel):
    
    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="سؤال المستخدم",
        examples=["What is FastAPI?"]
    )
    conversation_id: Optional[str] = Field(
        default=None,
        description="معرف المحادثة (لاستكمال محادثة سابقة)"
    )
    history: Optional[List[Dict[str, str]]] = Field(
        default=None,
        description="تاريخ يدوي: [{'role': 'user', 'content': '...'}]"
    )


class SourceInfo(BaseModel):
    """معلومات عن مصدر مستخدم في الإجابة."""
    content: str
    source: str
    score: float = Field(..., ge=0, le=1)


class ChatResponse(BaseModel):
    """رد المحادثة — الإجابة + المصادر + الثقة."""
    answer: str
    sources: List[SourceInfo]
    confidence: float = Field(..., ge=0, le=1)
    conversation_id: str


class ConversationMessage(BaseModel):
    """رسالة واحدة في سجل المحادثة."""
    role: str
    content: str


class ConversationResponse(BaseModel):
    """سجل محادثة كامل."""
    conversation_id: str
    title: Optional[str] = None
    messages: List[ConversationMessage]
    total_messages: int
