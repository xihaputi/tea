import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect

# 1. Load env
load_dotenv()
db_url = os.getenv("DB_URL")
if not db_url:
    # Fallback if not set (though it should be)
    db_url = "mysql+pymysql://root:yang123.@localhost:3306/tea"

print(f"Connecting to: {db_url}")
engine = create_engine(db_url)

def fix_table_schema():
    with engine.connect() as conn:
        inspector = inspect(engine)
        columns = [c['name'] for c in inspector.get_columns("rules")]
        print(f"Current columns in 'rules': {columns}")
        
        # Check and add product_id
        if "product_id" not in columns:
            print("Adding column product_id...")
            conn.execute(text("ALTER TABLE rules ADD COLUMN product_id INT NULL"))
        else:
            print("Column product_id already exists.")
            
        # Check and add device_id
        if "device_id" not in columns:
            print("Adding column device_id...")
            conn.execute(text("ALTER TABLE rules ADD COLUMN device_id INT NULL"))
            
        # Check and add input_key
        if "input_key" not in columns:
            print("Adding column input_key...")
            conn.execute(text("ALTER TABLE rules ADD COLUMN input_key VARCHAR(50) NULL"))
            
        # Check and add operator
        if "operator" not in columns:
            print("Adding column operator...")
            conn.execute(text("ALTER TABLE rules ADD COLUMN operator VARCHAR(10) NULL"))

        # Check and add threshold
        if "threshold" not in columns:
            print("Adding column threshold...")
            conn.execute(text("ALTER TABLE rules ADD COLUMN threshold FLOAT NULL"))
            
        conn.commit()
        print("Schema fix complete.")

if __name__ == "__main__":
    fix_table_schema()
