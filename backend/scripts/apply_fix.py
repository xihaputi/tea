# -*- coding: utf-8 -*-
import sqlite3
import os
import sys

# Ensure we use the correct path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
DB_PATH = os.path.join(backend_dir, "tea_garden.db")

def fix():
    print(f"Connecting to {DB_PATH}", flush=True)
    if not os.path.exists(DB_PATH):
        print("Error: DB not found", flush=True)
        return

    try:
        conn = sqlite3.connect(DB_PATH, timeout=10) # 10s timeout
        cursor = conn.cursor()
        
        # Enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")
        
        print("Creating categories...", flush=True)
        # 1. Categories
        # 监测类 \u76d1\u6d4b\u7c7b
        # 控制类 \u63a7\u5236\u7c7b
        cursor.execute("INSERT OR IGNORE INTO products (id, name, parent_id) VALUES (10, '\u76d1\u6d4b\u7c7b', NULL)")
        cursor.execute("INSERT OR IGNORE INTO products (id, name, parent_id) VALUES (11, '\u63a7\u5236\u7c7b', NULL)")
        
        print("Updating existing products...", flush=True)
        # 2. Update existing
        # 土壤检测仪 \u571f\u58e4\u68c0\u6d4b\u4eea
        cursor.execute("UPDATE products SET name='\u571f\u58e4\u68c0\u6d4b\u4eea', parent_id=10 WHERE id=1")
        print(f"Updated Soil (rowcount: {cursor.rowcount})", flush=True)
        
        # 茶园气象站 \u8336\u56ed\u6c14\u8c61\u7ad9
        cursor.execute("UPDATE products SET name='\u8336\u56ed\u6c14\u8c61\u7ad9', parent_id=10 WHERE id=2")
        print(f"Updated Weather (rowcount: {cursor.rowcount})", flush=True)
        
        # 水肥一体机 \u6c34\u80a5\u4e00\u4f53\u673a
        cursor.execute("UPDATE products SET name='\u6c34\u80a5\u4e00\u4f53\u673a', parent_id=11 WHERE id=3")
        print(f"Updated WaterFit (rowcount: {cursor.rowcount})", flush=True)
        
        # 3. Create Valve
        # 阀门 \u9600\u95e8
        cursor.execute("INSERT OR IGNORE INTO products (id, name, parent_id) VALUES (4, '\u9600\u95e8', 11)")
        cursor.execute("UPDATE products SET name='\u9600\u95e8', parent_id=11 WHERE id=4")
        print(f"Upserted Valve (rowcount: {cursor.rowcount})", flush=True)
        
        conn.commit()
        print("Committed changes.", flush=True)
        
        # Check
        cursor.execute("SELECT id, name, parent_id FROM products")
        rows = cursor.fetchall()
        print("Final State:", flush=True)
        for r in rows:
            print(r, flush=True)
            
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}", flush=True)

if __name__ == "__main__":
    fix()
