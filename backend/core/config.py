# from pydantic_settings import BaseSettings, SettingsConfigDict

# class Settings(BaseSettings):
#     DATABASE_URL: str
#     CELERY_BROKER_URL: str
#     CELERY_RESULT_BACKEND: str
#     GOOGLE_API_KEY: str

#     model_config = SettingsConfigDict(env_file=".env")

# settings = Settings()



from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # These variables will now be loaded from the Hugging Face secrets UI
    DATABASE_URL: str
    GOOGLE_API_KEY: str
    
    # These variables are hardcoded for the Hugging Face environment
    # because Redis is running in the same container.
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # This tells Pydantic to first look for system environment variables,
    # and then fall back to a .env file if one exists.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

settings = Settings()