from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class DbSettings(BaseModel):
    url: str = "postgresql+asyncpg://admin:admin@postgres:5432/t_clone_db"
    echo: bool = False


class Settings(BaseSettings):
    api_prefix: str = "/api"

    db: DbSettings = DbSettings()

    static_image_dir: Path = BASE_DIR / "static" / "images"

    file_save_prefix: str = "/static/images/"

    allowed_extensions: set = ("jpg", "png", "gif", "jpeg",)

    upload_all_tweets: float = False


settings = Settings()
settings.upload_all_tweets = True
