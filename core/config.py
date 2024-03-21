from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent


class DbSettings(BaseModel):
    url: str = "postgresql+asyncpg://admin:admin@localhost"
    echo: bool = False


class Settings(BaseSettings):
    api_prefix: str = "/api"

    db: DbSettings = DbSettings()

    templates_dir: Path = BASE_DIR / "templates"
    static_dir: Path = BASE_DIR / "static"
    image_dir: Path = static_dir / "images"


settings = Settings()
