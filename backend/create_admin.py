from app.database import SessionLocal
from app.models import User
import json

def create_admin():
    db = SessionLocal()
    try:
        # Check if admin exists
        user = db.query(User).filter(User.username == "admin").first()
        if user:
            print("Admin user already exists.")
            return

        admin_user = User(
            username="admin",
            password="admin123",
            name="Super Admin",
            roles="admin",
            permissions=json.dumps(["*"])
        )
        db.add(admin_user)
        db.commit()
        print("Admin user created: admin / admin123")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
