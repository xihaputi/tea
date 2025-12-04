import sqlite3
import os

# Database file path
DB_FILE = "tea_garden.db"

def add_column():
    if not os.path.exists(DB_FILE):
        print(f"Database file {DB_FILE} not found.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(tea_gardens)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "image_path" in columns:
            print("Column 'image_path' already exists.")
        else:
            print("Adding column 'image_path'...")
            cursor.execute("ALTER TABLE tea_gardens ADD COLUMN image_path VARCHAR(255)")
            conn.commit()
            print("Column added successfully.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_column()
