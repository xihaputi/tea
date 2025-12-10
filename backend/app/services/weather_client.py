import httpx
import logging

logger = logging.getLogger(__name__)

async def get_weather_forecast(location: str) -> dict:
    """
    Fetch weather from wttr.in (JSON format).
    wttr.in returns a complex JSON, we extract simple current condition.
    """
    try:
        # format=j1 returns a specific JSON format
        url = f"https://wttr.in/{location}?format=j1&lang=zh"
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            
            # Extract current condition
            current = data.get('current_condition', [{}])[0]
            temp_c = current.get('temp_C', 'N/A')
            desc = current.get('lang_zh', [{'value': '未知'}])[0]['value']
            humidity = current.get('humidity', '0')
            wind_speed = current.get('windspeedKmph', '0') # wttr.in gives kmph usually
            
            # Wind power estimate (Beaufort scale rough mapping)
            try:
                wind_kmph = float(wind_speed)
                if wind_kmph < 1: wind_power = 0
                elif wind_kmph < 6: wind_power = 1
                elif wind_kmph < 12: wind_power = 2
                elif wind_kmph < 20: wind_power = 3
                elif wind_kmph < 29: wind_power = 4
                else: wind_power = 5
            except:
                wind_power = 0

            return {
                "location": location,
                "temperature": temp_c,
                "weather": desc,
                "humidity": humidity,
                "windPower": str(wind_power)
            }
            
    except Exception as e:
        logger.warning(f"Failed to fetch weather for {location}: {e}. Retrying with default location 'Xinyang'.")
        # Retry with Xinyang as fallback
        if location != "Xinyang":
            try:
                return await get_weather_forecast("Xinyang")
            except:
                pass

        logger.error(f"Failed to fetch weather definitively: {e}")
        # Return fallback data so the UI doesn't break
        return {
            "location": location,
            "temperature": "--",
            "weather": "数据获取失败",
            "humidity": "-",
            "windPower": "-"
        }

