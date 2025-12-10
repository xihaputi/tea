import os
import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles

router = APIRouter(prefix="/upload", tags=["upload"])

# Upload directory
UPLOAD_DIR = "static/uploads"
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

@router.post("")
async def upload_file(file: UploadFile = File(...)):
    """
    上传文件
    Upload file
    """
    try:
        # Generate unique filename
        file_ext = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Return URL (assuming static files are served from /static)
        return {"url": f"/static/uploads/{filename}", "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
