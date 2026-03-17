from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    api_title: str = "Business Intelligence Dashboard API"
    api_version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # LLM Configuration
    gemini_api_key: str
    
    # Database Configuration
    database_type: str = "sqlite"  # sqlite, postgresql, csv
    database_url: str = "sqlite:///./bi_dashboard.db"
    
    # CSV Data Configuration
    csv_data_path: str = "./data/"
    
    # CORS Configuration
    cors_origins: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Load settings
settings = Settings()
