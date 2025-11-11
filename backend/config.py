import json

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration de l'application avec pydantic-settings"""

    # Application
    PROJECT_NAME: str = "Tools API"
    PROJECT_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # API
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",  # Next.js
        "http://localhost:4321",  # Astro
        "http://localhost:8000",  # FastAPI lui-même
    ]

    # Sécurité
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # Base de données (optionnel)
    DATABASE_URL: str | None = None

    # Email (optionnel)
    SMTP_SERVER: str | None = None
    SMTP_PORT: int | None = 587
    SMTP_USERNAME: str | None = None
    SMTP_PASSWORD: str | None = None
    FROM_EMAIL: str | None = None

    # Logging
    LOG_LEVEL: str = "INFO"
    ENABLE_ANALYTICS: bool = True

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                pass
        return v

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v):
        if v and "postgresql" in v and "://" not in v:
            raise ValueError("DATABASE_URL must be a valid URL")
        return v

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instance globale des settings
settings = Settings()

# Configuration pour le logging
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "default": {
            "level": settings.LOG_LEVEL,
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {  # Root logger
            "handlers": ["default"],
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["default"],
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
        "fastapi": {
            "handlers": ["default"],
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
    },
}
