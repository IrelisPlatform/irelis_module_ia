from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "IRELIS Module IA"
    environment: str = "local"
    database_url: str = "sqlite:///./app.db"
    secret_key: str = "changeme"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
