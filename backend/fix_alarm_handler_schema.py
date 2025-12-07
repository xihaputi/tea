import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect

# Load env to get DB_URL
load_dotenv()
db_url = os.getenv("DB_URL") or "mysql+pymysql://root:yang123.@localhost:3306/tea"

print(f"Connecting to: {db_url}")
engine = create_engine(db_url)

def fix_alarm_schema():
    with engine.connect() as conn:
        inspector = inspect(engine)
        columns = [c['name'] for c in inspector.get_columns("alarms")]
        print(f"Current columns in 'alarms': {columns}")
        
        if "handler_id" not in columns:
            print("Adding column handler_id...")
            conn.execute(text("ALTER TABLE alarms ADD COLUMN handler_id INT NULL"))
            # Optionally add foreign key constraint, but kept simple for now
        else:
            print("Column handler_id already exists.")
            
        conn.commit()
        print("Alarm schema fix complete.")

if __name__ == "__main__":
    fix_alarm_schema()
