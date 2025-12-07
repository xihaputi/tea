# -*- coding: utf-8 -*-
import sqlite3
import os
import json

# Ensure we use the correct path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
DB_PATH = os.path.join(backend_dir, "tea_garden.db")

def apply_defaults():
    print("Connecting to DB...")
    if not os.path.exists(DB_PATH):
        print("Error: DB not found")
        return

    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        cursor = conn.cursor()
        
        # 1. Soil Sensor Defaults
        soil_config = {
            "soil_humi": {"name": "\u571f\u58e4\u542b\u6c34\u91cf", "unit": "%", "show": True},
            "soil_temp": {"name": "\u571f\u58e4\u6e29\u5ea6", "unit": "\u2103", "show": True},
            "soil_ph": {"name": "\u571f\u58e4PH", "unit": "", "show": True},
            "soil_ec": {"name": "\u571f\u58e4EC", "unit": "us/cm", "show": True}
        }
        soil_json = json.dumps(soil_config, ensure_ascii=False)
        
        cursor.execute("UPDATE devices SET sensor_config = ? WHERE product_id = 1", (soil_json,))
        print("Updated Soil Sensors")
        
        # 2. Weather Station Defaults
        weather_config = {
            "air_temp": {"name": "\u7a7a\u6c14\u6e29\u5ea6", "unit": "\u2103", "show": True},
            "humidity": {"name": "\u76f8\u5bf9\u6e7f\u5ea6", "unit": "%", "show": True},
            "rainfall": {"name": "\u964d\u96e8\u91cf", "unit": "mm", "show": True},
            "lux": {"name": "\u5149\u7167\u5f3a\u5ea6", "unit": "Lux", "show": True},
            "wind_speed": {"name": "\u98ce\u901f", "unit": "m/s", "show": True},
            "wind_dir": {"name": "\u98ce\u5411", "unit": "\u00b0", "show": True}
        }
        weather_json = json.dumps(weather_config, ensure_ascii=False)
        
        cursor.execute("UPDATE devices SET sensor_config = ? WHERE product_id = 2", (weather_json,))
        print("Updated Weather Stations")
        
        conn.commit()
        conn.close()
        print("Done.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    apply_defaults()
