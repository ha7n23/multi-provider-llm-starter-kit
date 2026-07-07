import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""

    app_name: str = os.getenv("APP_NAME", "Multi-Provider LLM Starter Kit")
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()
    default_provider: str = os.getenv("DEFAULT_PROVIDER", "mock").lower()
    max_output_tokens: int = int(os.getenv("MAX_OUTPUT_TOKENS", 300))


settings = Settings()