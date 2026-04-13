from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    All project-wide settings here
    """

    # App metadata
    PROJECT_NAME: str = "Books Store API"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = (
        "A professional FastAPI-based REST API for managing "
        "books, authors, and reviews."
    )
    
    # API Version
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "sqllite:///./books_store.db"

    # Panigation defaults
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()