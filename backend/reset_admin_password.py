from app.database import SessionLocal
from app.models import User
import json

def reset_admin():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "admin").first()
        if user:
            print(f"Found admin user. Old password: {user.password}")
            user.password = "admin123"
            user.permissions = json.dumps(["*"])
            db.commit()
            print("Admin password reset to: admin123")
        else:
            print("Admin user not found. Creating...")
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
    reset_admin()
