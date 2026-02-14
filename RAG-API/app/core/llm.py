from typing import AsyncGenerator, List
import httpx
import json

from app.config import get_settings
from app.models.conversation import Message

settings = get_settings()

class OllamaLLM:
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.llm_model
        self.client = httpx.AsyncClient(
            base_url=settings.ollama_base_url,
            timeout=120.0
        )

    async def generate(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        
        formatted = [{"role": m.role, "content": m.content} for m in messages]

        response = await self.client.post(
            "/api/chat",
            json={
                "model": self.model_name,
                "messages": formatted,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
        )
        response.raise_for_status()
        return response.json()["message"]["content"]

    async def stream(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> AsyncGenerator[str, None]:
        
        formatted = [{"role": m.role, "content": m.content} for m in messages]

        async with self.client.stream(
            "POST",
            "/api/chat",
            json={
                "model": self.model_name,
                "messages": formatted,
                "stream": True,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
        ) as response:
            async for line in response.aiter_lines():
                if line.strip():
                    data = json.loads(line)
                    if "message" in data and data["message"].get("content"):
                        yield data["message"]["content"]


# Singleton
llm = OllamaLLM()
