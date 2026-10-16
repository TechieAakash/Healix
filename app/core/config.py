from typing import List, Union, Optional
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import json


class Settings(BaseSettings):
    PROJECT_NAME: str = "Healix Healthcare Triage Assistant API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./healix.db"

    # JWT Authentication
    JWT_SECRET_KEY: str = "development_jwt_secret_key_healix_production_standard_2026_xyz"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, str) and v.startswith("["):
            return json.loads(v)
        elif isinstance(v, list):
            return v
        return []

    # AI & Vector DB Integrations
    AI_PROVIDER: str = "mock"
    AI_API_KEY: str = ""
    AI_MODEL: str = "gpt-4o-mini"
    AI_TEMPERATURE: float = 0.2
    AI_MAX_TOKENS: int = 2048
    AI_BASE_URL: Optional[str] = None
    AI_REQUEST_TIMEOUT: float = 30.0
    AI_MAX_RETRIES: int = 2

    # Embeddings & RAG Vector DB
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    VECTOR_DB_URL: str = ""
    VECTOR_DB_PATH: str = "data/vector_store.json"
    RAG_TOP_K: int = 4
    SIMILARITY_THRESHOLD: float = 0.25
    ENABLE_RAG_RERANKING: bool = True

    # Prompt Engineering
    PROMPT_VERSION: str = "v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
