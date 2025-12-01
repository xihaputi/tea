from app.database import engine
from sqlalchemy import text

def migrate_db():
    with engine.connect() as conn:
        try:
            # ³¢ÊÔÌí¼Ó mqtt_username ÁÐ
            conn.execute(text("ALTER TABLE devices ADD COLUMN mqtt_username VARCHAR(100)"))
            print("Added mqtt_username column.")
        except Exception as e:
            print(f"mqtt_username column might already exist: {e}")

        try:
            # ³¢ÊÔÌí¼Ó mqtt_password ÁÐ
            conn.execute(text("ALTER TABLE devices ADD COLUMN mqtt_password VARCHAR(100)"))
            print("Added mqtt_password column.")
        except Exception as e:
            print(f"mqtt_password column might already exist: {e}")
            
        conn.commit()

if __name__ == "__main__":
    print("Migrating database...")
    migrate_db()
    print("Migration complete.")
