from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from ..schemas import DiseasePrediction
from ..services.disease_model import DiseaseModel
from ..utils.file_utils import save_upload_file

router = APIRouter(prefix="/disease", tags=["disease"])
disease_model = DiseaseModel()


@router.post("/detect", response_model=DiseasePrediction)
async def detect_disease(file: UploadFile = File(...), plot_id: int | None = None) -> DiseasePrediction:
    """
    病虫害识别接口
    Disease detection endpoint
    """
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="仅支持图片上传 / Only image uploads are supported")

    saved_path: Path = await save_upload_file(file)
    result = disease_model.predict(saved_path)
    return DiseasePrediction(
        disease_type=result["disease_type"],
        confidence=result["confidence"],
        advice=result["advice"],
        image_url=str(saved_path),
        plot_id=plot_id,
        timestamp=datetime.now(timezone.utc),
    )
