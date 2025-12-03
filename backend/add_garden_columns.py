from app.database import engine, Base
from sqlalchemy import text

def migrate():
    with engine.connect() as conn:
        # Check and add latitude
        try:
            conn.execute(text("ALTER TABLE tea_gardens ADD COLUMN latitude FLOAT"))
            print("Added latitude column")
        except Exception as e:
            print(f"latitude column might already exist: {e}")

        # Check and add longitude
        try:
            conn.execute(text("ALTER TABLE tea_gardens ADD COLUMN longitude FLOAT"))
            print("Added longitude column")
        except Exception as e:
            print(f"longitude column might already exist: {e}")

        # Check and add camera_url
        try:
            conn.execute(text("ALTER TABLE tea_gardens ADD COLUMN camera_url VARCHAR(255)"))
            print("Added camera_url column")
        except Exception as e:
            print(f"camera_url column might already exist: {e}")

if __name__ == "__main__":
    migrate()
