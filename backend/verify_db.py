from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.models import Base, TeaGarden, Device, Alarm
from app.config import settings

def verify():
    engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    inspector = inspect(engine)
    
    print("Checking tea_gardens columns...")
    columns = [c['name'] for c in inspector.get_columns('tea_gardens')]
    if 'image_path' in columns:
        print("SUCCESS: 'image_path' column exists.")
    else:
        print("FAILURE: 'image_path' column MISSING.")
        
    print("\nChecking relationships...")
    try:
        gardens = db.query(TeaGarden).limit(1).all()
        if not gardens:
            print("No gardens found to test.")
        else:
            garden = gardens[0]
            print(f"Garden: {garden.name}")
            print(f"Devices: {len(garden.devices)}")
            for device in garden.devices:
                print(f"  Device: {device.name}")
                # This is the critical part that might fail
                print(f"  Alarms: {len(device.alarms)}")
        print("SUCCESS: Relationships seem to work.")
    except Exception as e:
        print(f"FAILURE: Relationship check failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify()
