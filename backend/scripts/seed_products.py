import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tea_garden.db")

def seed():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("Seeding products...")
    
    # 1. Clear existing products (Optional: strictly speaking we should migrate, but for 'perfecting' let's reset to clean state)
    # But checking if we have devices...
    cursor.execute("SELECT count(*) FROM devices")
    cnt = cursor.fetchone()[0]
    print(f"Found {cnt} devices. Resetting product catalog...")
    
    cursor.execute("DELETE FROM products")
    
    # 2. Insert new hierarchy
    # 10: Monitor
    # 11: Control
    # 12: Weather
    # 13: Soil
    # 14: Valve
    # 15: WaterFit
    
    products = [
        (10, "监测类", None),
        (11, "控制类", None),
        (12, "茶园气象站", 10),
        (13, "土壤检测仪", 10),
        (14, "阀门", 11),
        (15, "水肥一体机", 11)
    ]
    
    cursor.executemany("INSERT INTO products (id, name, parent_id) VALUES (?, ?, ?)", products)
    
    conn.commit()
    conn.close()
    print("Done.")

if __name__ == "__main__":
    seed()
