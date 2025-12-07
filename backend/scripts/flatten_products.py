# -*- coding: utf-8 -*-
import sqlite3
import os

# Ensure we use the correct path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
DB_PATH = os.path.join(backend_dir, "tea_garden.db")

def flatten():
    print(f"Connecting to {DB_PATH}", flush=True)
    if not os.path.exists(DB_PATH):
        print("Error: DB not found", flush=True)
        return

    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        cursor = conn.cursor()
        
        # Enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")
        
        print("Flattening products...", flush=True)
        
        # 1. Update all concrete products to have NO parent
        # ID 1, 2, 3, 4 are our concrete products
        cursor.execute("UPDATE products SET parent_id = NULL WHERE id IN (1, 2, 3, 4)")
        print(f"Updated concrete products (rowcount: {cursor.rowcount})", flush=True)
        
        # 2. Delete Categories (10, 11)
        cursor.execute("DELETE FROM products WHERE id IN (10, 11)")
        print(f"Deleted categories (rowcount: {cursor.rowcount})", flush=True)
        
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
    flatten()
