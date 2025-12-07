import os
from dotenv import load_dotenv
from sqlalchemy import text, inspect

load_dotenv(".env")
print(f"Target DB: {os.getenv('DB_URL')}")

from app.database import engine

def add_column_if_not_exists(conn, table_name, col_name, col_def):
    try:
        inspector = inspect(engine)
        columns = [c['name'] for c in inspector.get_columns(table_name)]
        if col_name not in columns:
            print(f"Adding '{col_name}' to '{table_name}'...")
            conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_def}"))
            print(f"'{col_name}' added.")
        else:
            print(f"'{col_name}' already exists in '{table_name}'.")
    except Exception as e:
        print(f"Error checking/adding {col_name}: {e}")

def fix_all():
    with engine.connect() as conn:
        # tea_gardens columns
        add_column_if_not_exists(conn, "tea_gardens", "latitude", "FLOAT")
        add_column_if_not_exists(conn, "tea_gardens", "longitude", "FLOAT")
        add_column_if_not_exists(conn, "tea_gardens", "camera_url", "VARCHAR(255)")
        add_column_if_not_exists(conn, "tea_gardens", "image_path", "VARCHAR(255)")
        
        # devices columns
        add_column_if_not_exists(conn, "devices", "sensor_config", "TEXT")
        
        conn.commit()

if __name__ == "__main__":
    fix_all()
