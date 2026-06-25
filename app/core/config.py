from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "TrackFlow"
    app_version: str = "0.1.0"
    debug: bool = False

    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "trackflow"

    rabbitmq_uri: str = "amqp://guest:guest@localhost:5672/"

    speed_limit: float = 80.0

    api_v1_prefix: str = "/api/v1"


settings = Settings()
