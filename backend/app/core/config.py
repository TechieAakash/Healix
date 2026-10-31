from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Healix Explainable AI Health Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    JWT_SECRET: str = "healix-super-secret-key-change-in-production-2026-nsut-ai"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours for seamless demo/testing
    
    # Database: Defaults to async SQLite for local frictionless execution, supports Postgres
    DATABASE_URL: str = "sqlite+aiosqlite:///./healix.db"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]
    
    # Clinical Safety & Triage
    ENABLE_EMERGENCY_OVERRIDE: bool = True
    KB_DEFAULT_VERSION: str = "v2.0.0"
    DEFAULT_EMERGENCY_PHONE: str = "112"  # National Emergency Number (112 in India/EU, 911 configurable)

    # Gemini API Configuration
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"
    GEMINI_TIMEOUT_SECONDS: float = 12.0

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()

