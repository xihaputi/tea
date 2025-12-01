from pathlib import Path

from fastapi import UploadFile

from ..config import settings


# 确保上传目录存在
# Ensure upload directory exists
UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


async def save_upload_file(upload_file: UploadFile) -> Path:
    """
    保存上传的文件
    Save an uploaded file
    """
    destination = UPLOAD_DIR / upload_file.filename
    content = await upload_file.read()
    destination.write_bytes(content)
    return destination

