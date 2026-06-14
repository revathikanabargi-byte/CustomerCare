"""
Application Configuration Module
Centralized configuration management for the Customer Care Agent
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # API Configuration
    app_name: str = "Customer Care AI Agent"
    app_version: str = "2.0.0"
    debug: bool = False
    
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.0
    
    # Knowledge Base Configuration
    knowledge_base_path: str = "knowledge_base.txt"
    chunk_size: int = 300
    chunk_overlap: int = 50
    retrieval_k: int = 2
    
    # Memory Configuration
    max_conversation_memory: int = 5
    
    # Logging Configuration
    log_file: str = "app.log"
    log_level: str = "INFO"
    
    # Security Configuration
    unsafe_keywords: list[str] = [
        "hack",
        "bypass security",
        "steal",
        "disable mfa permanently",
        "exploit",
        "vulnerability"
    ]
    
    # CORS Configuration
    cors_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def validate_settings() -> bool:
    """Validate critical settings"""
    if not settings.openai_api_key:
        raise ValueError(
            "OPENAI_API_KEY not found in environment variables. "
            "Please create a .env file with your API key."
        )
    
    if not os.path.exists(settings.knowledge_base_path):
        raise FileNotFoundError(
            f"Knowledge base file not found: {settings.knowledge_base_path}"
        )
    
    return True

# Made with Bob
