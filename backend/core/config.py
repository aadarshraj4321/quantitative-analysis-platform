from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    GOOGLE_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()