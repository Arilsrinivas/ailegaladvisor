import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Legal Advisor (Nyaya AI)"
    API_V1_STR: str = "/api"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "nyaya-ai-super-secret-production-key-2026-legal-advisor")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database - Default to SQLite for seamless local execution; supports PostgreSQL if provided
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/legaladvisor.db")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Vector Search & Embeddings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_CACHE_DIR: str = "./models/embeddings"
    FAISS_INDEX_DIR: str = "./data/faiss_index"
    BM25_INDEX_FILE: str = "./data/bm25_index.pkl"
    
    # LLM & APIs
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")
    
    # Uploads & Storage
    UPLOAD_DIR: str = "./data/uploads"
    LOG_DIR: str = "./logs/compliance"
    
    # Supported Languages
    SUPPORTED_LANGUAGES: List[str] = [
        "en",  # English
        "hi",  # Hindi
        "ta",  # Tamil
        "te",  # Telugu
        "bn",  # Bengali
        "mr",  # Marathi
        "gu",  # Gujarati
        "kn"   # Kannada
    ]
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "*"
    ]

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"

settings = Settings()
