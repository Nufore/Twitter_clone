from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_prefix: str = "/api"

    db_url: str = "postgresql+asyncpg://admin:admin@localhost"
    db_echo: bool = True


settings = Settings()
