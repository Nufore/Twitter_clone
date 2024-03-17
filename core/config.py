from pydantic import BaseModel
from pydantic_settings import BaseSettings


class DbSettings(BaseModel):
    url: str = "postgresql+asyncpg://admin:admin@localhost"
    echo: bool = False


class Settings(BaseSettings):
    api_prefix: str = "/api"

    db: DbSettings = DbSettings()


settings = Settings()
