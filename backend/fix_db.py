from app.database import engine, Base
from app.models import Rule, Alarm
from sqlalchemy import text

def reset_rules_table():
    with engine.connect() as conn:
        print("Dropping rules table...")
        conn.execute(text("DROP TABLE IF EXISTS rules"))
        conn.execute(text("DROP TABLE IF EXISTS alarms")) # Drop alarms too just in case of foreign key issues
        conn.commit()
        print("Tables dropped.")

if __name__ == "__main__":
    reset_rules_table()
    print("Please restart the backend to recreate tables.")
