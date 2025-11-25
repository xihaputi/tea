from pathlib import Path

from fastapi import UploadFile

from ..config import get_settings

settings = get_settings()
settings.upload_dir.mkdir(parents=True, exist_ok=True)


async def save_upload_file(upload_file: UploadFile) -> Path:
    """Save an uploaded file to the uploads directory."""
    destination = settings.upload_dir / upload_file.filename
    content = await upload_file.read()
    destination.write_bytes(content)
    return destination

