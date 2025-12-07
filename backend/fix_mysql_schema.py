import os
from dotenv import load_dotenv
from sqlalchemy import text, inspect

# Load env vars explicitly
load_dotenv(".env")

from app.database import engine, Base
from app.models import User  # Import models to ensure they are registered in Base

def fix_schema():
    print(f"Connecting to: {os.getenv('DB_URL')}")
    
    with engine.connect() as conn:
        # 1. Check and add permissions column
        try:
            # Check if column exists
            inspector = inspect(engine)
            columns = [c['name'] for c in inspector.get_columns('users')]
            if 'permissions' not in columns:
                print("Adding 'permissions' column to 'users' table...")
                conn.execute(text("ALTER TABLE users ADD COLUMN permissions TEXT"))
                print("'permissions' column added.")
            else:
                print("'permissions' column already exists.")
        except Exception as e:
            print(f"Error checking/adding column: {e}")

    # 2. Create missing tables (e.g., user_gardens)
    print("Creating missing tables...")
    Base.metadata.create_all(bind=engine)
    print("Missing tables created (if any).")

if __name__ == "__main__":
    fix_schema()
