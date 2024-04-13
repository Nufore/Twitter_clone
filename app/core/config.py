import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()
BASE_DIR = Path(__file__).parent.parent
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


class DbSettings(BaseModel):
    url: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    echo: bool = False


class Settings(BaseSettings):
    api_prefix: str = "/api"

    db: DbSettings = DbSettings()

    static_image_dir: Path = BASE_DIR / "static" / "images"

    file_save_prefix: str = "/static/images/"

    allowed_extensions: set = {"jpg", "png", "gif", "jpeg"}

    upload_all_tweets: float = False


settings = Settings()
settings.upload_all_tweets = True
