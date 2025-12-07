import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tea_garden.db")

def fix():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("Fixing products...")
    
    # 1. Ensure Categories exist
    # 10: Monitor, 11: Control
    cursor.execute("INSERT OR IGNORE INTO products (id, name, parent_id) VALUES (10, '监测类', NULL)")
    cursor.execute("INSERT OR IGNORE INTO products (id, name, parent_id) VALUES (11, '控制类', NULL)")
    
    # 2. Update existing products to new names and structure
    # ID 1: 土壤传感器 v1 -> 土壤检测仪 (Parent 10)
    cursor.execute("UPDATE products SET name='土壤检测仪', parent_id=10 WHERE id=1")
    
    # ID 2: 茶园气象站 v2 -> 茶园气象站 (Parent 10)
    cursor.execute("UPDATE products SET name='茶园气象站', parent_id=10 WHERE id=2")
    
    # ID 3: 水肥一体机 -> 水肥一体机 (Parent 11)
    cursor.execute("UPDATE products SET name='水肥一体机', parent_id=11 WHERE id=3")
    
    # 3. Create 'Valve' if not exists (ID 4, Parent 11)
    # Check if ID 4 exists, if so update, else insert
    cursor.execute("INSERT OR IGNORE INTO products (id, name, parent_id) VALUES (4, '阀门', 11)")
    cursor.execute("UPDATE products SET name='阀门', parent_id=11 WHERE id=4")
    
    # 4. Clean up any weird ones if necessary, but safetly
    
    conn.commit()
    
    # Verify
    cursor.execute("SELECT id, name, parent_id FROM products")
    rows = cursor.fetchall()
    print("Current Products:")
    for r in rows:
        print(r)
        
    conn.close()
    print("Done.")

if __name__ == "__main__":
    fix()
