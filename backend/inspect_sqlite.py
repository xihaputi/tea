import sqlite3

db_path = "d:/thingsboard_envor/tea/backend/tea_garden.db"

def inspect_db():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"Database: {db_path}")
        print("-" * 50)
        
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")
            
            # Get columns
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            # cid, name, type, notnull, dflt_value, pk
            print(f"{'Column':<20} {'Type':<15} {'Nullable':<10} {'PK':<5}")
            print("-" * 50)
            for col in columns:
                print(f"{col[1]:<20} {col[2]:<15} {str(not col[3]):<10} {str(bool(col[5])):<5}")
                
        conn.close()
    except Exception as e:
        print(f"Error inspecting DB: {e}")

if __name__ == "__main__":
    inspect_db()
