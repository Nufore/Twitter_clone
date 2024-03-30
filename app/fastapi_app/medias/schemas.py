from pydantic import BaseModel
from app.core.config import settings


class FileSchema(BaseModel):
    filename: str
    content_type: str

    def check_content_type(self) -> dict:
        if (
            self.filename.rsplit(".", 1)[1] in settings.allowed_extensions
            and "image" in self.content_type
        ):
            return {"result": True}

        return {
            "result": False,
            "detail": f"wrong media data. allowed file extensions: .{' .'.join(settings.allowed_extensions)}",
        }
