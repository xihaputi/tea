from fastapi import APIRouter, Query
from app.services.weather_client import get_weather_forecast

router = APIRouter(
    prefix="/api/weather",
    tags=["Weather"]
)

@router.get("")
async def get_weather(location: str = Query("信阳", description="City name or location")):
    """
    Get current weather for a specific location.
    Defaults to '信阳' (Xinyang).
    """
    return await get_weather_forecast(location)
