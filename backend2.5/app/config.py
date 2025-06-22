from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:3245@localhost/postgres"
    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    elevenlabs_api_key: Optional[str] = None
    redis_url: str = "redis://localhost:6379"
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_bucket_name: Optional[str] = None
    aws_region: str = "us-east-1"
    secret_key: str = "1234567812345678"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()