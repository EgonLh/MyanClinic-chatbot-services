from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "RAG + Medicine Identifier"
    ENV: str = "development"
    DEBUG: bool = True
    OPENAI_API_KEY: str | None = None
    DATABASE_URL: str | None = None

    HF_API_KEY: str | None = None  # <- add this

    class Config:
        env_file = ".env"

settings = Settings()
