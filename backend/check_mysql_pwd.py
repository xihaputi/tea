import os
from dotenv import load_dotenv

# Load env before importing app.database
load_dotenv(".env")
print(f"Loaded DB_URL: {os.getenv('DB_URL')}")

from app.database import SessionLocal
from app.models import User

def check_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"{'ID':<5} {'Username':<15} {'Password':<15} {'Role':<15}")
        print("-" * 50)
        for user in users:
            print(f"{user.id:<5} {user.username:<15} {user.password:<15} {user.roles:<15}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_users()
