def evaluate_soil_moisture(soil_moisture: float) -> dict:
    """Very simple rule engine for irrigation advice."""
    if soil_moisture < 30:
        return {"level": "water", "advice": "Soil is dry, schedule watering today."}
    if 30 <= soil_moisture <= 70:
        return {"level": "optimal", "advice": "Moisture is within the optimal range."}
    return {"level": "drain", "advice": "Soil is too wet, pause watering and check drainage."}

