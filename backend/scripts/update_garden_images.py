import sqlite3
import random
import os

DB_PATH = "tea_garden.db"

def update_images():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Get all gardens
        cursor.execute("SELECT id, name FROM tea_gardens")
        gardens = cursor.fetchall()
        
        print(f"Found {len(gardens)} tea gardens.")
        
        for garden in gardens:
            g_id, g_name = garden
            # Assign random image from 1 to 14
            img_idx = random.randint(1, 14)
            image_path = f"/static/gardens/{img_idx}.png"
            
            cursor.execute("UPDATE tea_gardens SET image_path = ? WHERE id = ?", (image_path, g_id))
            print(f"Updated Garden {g_id} ({g_name}) -> {image_path}")
            
        conn.commit()
        print("All gardens updated successfully.")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    update_images()
