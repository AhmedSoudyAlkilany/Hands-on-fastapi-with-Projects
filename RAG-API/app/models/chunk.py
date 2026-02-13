from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class Chunk:
   
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    chunk_index: int = 0
    total_chunks: int = 0

    @property
    def source(self) -> str:
        return self.metadata.get("source", "unknown")


@dataclass
class SearchResult:
    
    id: str
    content: str
    metadata: Dict[str, Any]
    score: float

    @property
    def source(self) -> str:
        return self.metadata.get("source", "unknown")


@dataclass
class RAGResponse:
    
    answer: str
    sources: List[Dict[str, Any]]
    confidence: float