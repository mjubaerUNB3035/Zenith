from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Zenith"
    app_env: str = "development"

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()