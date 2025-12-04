from app.database import engine, Base
from app.models import User
from sqlalchemy import text

def reset_users_table():
    with engine.connect() as conn:
        print("Dropping users and user_gardens tables...")
        conn.execute(text("DROP TABLE IF EXISTS user_gardens"))
        conn.execute(text("DROP TABLE IF EXISTS users"))
        conn.commit()
        print("Tables dropped.")

if __name__ == "__main__":
    reset_users_table()
    print("Please restart the backend to recreate tables.")
