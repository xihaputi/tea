import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tea_garden.db")

def check():
    print(f"Checking DB at: {DB_PATH}")
    if not os.path.exists(DB_PATH):
        print("DB file not found!")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, parent_id FROM products")
    rows = cursor.fetchall()
    print("--- Products Table ---")
    for r in rows:
        print(r)
    print("----------------------")
    
    conn.close()

if __name__ == "__main__":
    check()
