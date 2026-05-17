from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = "development"
    DEBUG: bool = True
    LLM_PROVIDER: str = "openai"
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_API_KEY: str = ""
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/rag.db"
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 100
    TOP_K_CHUNKS: int = 5

    class Config:
        env_file = ".env"


settings = Settings()