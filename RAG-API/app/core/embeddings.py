from typing import List
import httpx

from app.config import get_settings

settings = get_settings()


class OllamaEmbeddings:
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.embedding_model
        self.client = httpx.AsyncClient(
            base_url=settings.ollama_base_url,
            timeout=120.0  
        )
        self._dimension = 768  

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        
        if not texts:
            return []

        response = await self.client.post(
            "/api/embed",
            json={"model": self.model_name, "input": texts}
        )
        response.raise_for_status()
        return response.json()["embeddings"]

    async def embed_query(self, text: str) -> List[float]:
        result = await self.embed_documents([text])
        return result[0]

    @property
    def dimension(self) -> int:
        return self._dimension


embeddings = OllamaEmbeddings()
