"""Configuration management for NexusOps Agent backend."""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings."""
    
    # MongoDB
    mongodb_uri: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    mongodb_database: str = "nexusops"
    mongodb_mcp_url: str = os.getenv("MONGODB_MCP_URL", "http://localhost:3100")
    
    # Google Cloud (optional)
    google_cloud_project: str = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    vertex_ai_location: str = os.getenv("VERTEX_AI_LOCATION", "us-central1")
    google_application_credentials: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    
    # API
    cors_origins: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")
    api_prefix: str = "/api"
    
    # Agent
    default_model: str = "gemini-2.0-flash-exp"
    fallback_model: str = "gemini-1.5-pro"
    max_tokens: int = 8192
    temperature: float = 0.7
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "nexusops-dev-secret-key")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7


settings = Settings()
