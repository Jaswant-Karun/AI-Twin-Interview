import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # App
    APP_NAME: str = "AI Interview Twin"
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://interview_user:interview_password@localhost:5432/ai_interview_db"
    )
    
    # APIs
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # URLs
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
