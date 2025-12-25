from pydantic_settings import BaseSettings
from pydantic import field_validator, computed_field
from typing import List
import json


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://emlakcrm:emlakcrm123@localhost:5432/emlakcrm_db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS - str olarak oku, sonra parse et (Pydantic Settings List[str] için JSON bekler)
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    
    # External APIs
    TKGM_API_URL: str = ""  # TKGM API endpoint (if available)
    MAPBOX_ACCESS_TOKEN: str = ""  # Mapbox token for additional services
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    @computed_field
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS from string (comma-separated) or JSON array"""
        if not self.CORS_ORIGINS or self.CORS_ORIGINS.strip() == "":
            return ["http://localhost:3000", "http://localhost:3001"]
        
        # Try JSON first
        try:
            parsed = json.loads(self.CORS_ORIGINS)
            if isinstance(parsed, list):
                return parsed
        except (json.JSONDecodeError, ValueError):
            pass
        
        # If not JSON, treat as comma-separated string
        return [origin.strip() for origin in self.CORS_ORIGINS.split(',') if origin.strip()]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

