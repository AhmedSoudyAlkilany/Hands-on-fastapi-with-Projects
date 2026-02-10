from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    # app 
    app_name: str = "AI Knowledge Base"
    debug: bool = False

    # Ollama 
    ollama_base_url: str = "http://localhost:11434"
    llm_model: str = "llama3.2"
    embedding_model: str = "nomic-embed-text"

    # Vector Store 
    chroma_persist_dir: str = "./data/chroma"
    collection_name: str = "knowledge_base"

    # RAG
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k: int = 5
    similarity_threshold: float = 0.3

    # memory
    max_conversation_history: int = 10

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    
    return Settings()
