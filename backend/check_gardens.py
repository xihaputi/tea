from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import TeaGarden
from app.config import settings

def check():
    engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        gardens = db.query(TeaGarden).all()
        print(f"Total Gardens: {len(gardens)}")
        for g in gardens:
            print(f"ID: {g.id}, Name: {g.name}, Created: {g.created_at}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check()
