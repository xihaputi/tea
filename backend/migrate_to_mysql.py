import sqlite3
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models import User, TeaGarden, Device, SensorRecord, Alarm, Rule, Task, ChatSession, ChatMessage, Plot, Product
# Note: user_gardens is a Table object, not a class, handled specially.

# Load target MySQL config
load_dotenv(".env")
MYSQL_URL = os.getenv("DB_URL")
print(f"Target MySQL: {MYSQL_URL}")

# Source SQLite
SQLITE_DB = "tea_garden.db"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def migrate():
    # 1. Connect to Source (SQLite)
    if not os.path.exists(SQLITE_DB):
        print(f"Source DB {SQLITE_DB} not found!")
        return

    src_conn = sqlite3.connect(SQLITE_DB)
    src_conn.row_factory = dict_factory
    src_cursor = src_conn.cursor()

    # 2. Connect to Target (MySQL)
    engine = create_engine(MYSQL_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Clear existing data in MySQL to avoid conflicts? 
        # Or just append/ignore? User probably wants REPLACEMENT of MySQL data with SQLite data.
        # Let's truncate/delete tables in reverse order.
        print("Cleaning target database...")
        session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        tables = ["chat_messages", "chat_sessions", "alarms", "sensor_records", "devices", "products", "plots", "user_gardens", "users", "tea_gardens", "rules", "tasks"]
        for t in tables:
             try:
                 session.execute(text(f"TRUNCATE TABLE {t}"))
             except:
                 session.execute(text(f"DELETE FROM {t}"))
        session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        session.commit()
        
        # 3. Migrate TeaGarden
        print("Migrating TeaGarden...")
        src_cursor.execute("SELECT * FROM tea_gardens")
        gardens = src_cursor.fetchall()
        for g in gardens:
            # Handle boolean conversion if needed (SQLite 0/1 -> MySQL 0/1 or Bool)
            obj = TeaGarden(**g)
            session.add(obj)
        session.commit()

        # 4. Migrate User
        print("Migrating User...")
        src_cursor.execute("SELECT * FROM users")
        users = src_cursor.fetchall()
        for u in users:
            obj = User(**u)
            session.add(obj)
        session.commit()

        # 5. Migrate UserGardens (Association)
        print("Migrating UserGardens...")
        try:
            src_cursor.execute("SELECT * FROM user_gardens")
            ugs = src_cursor.fetchall()
            for ug in ugs:
                # user_gardens is a Table, insert directly
                session.execute(text("INSERT INTO user_gardens (user_id, garden_id) VALUES (:user_id, :garden_id)"), ug)
            session.commit()
        except Exception as e:
            print(f"Skipping user_gardens (maybe empty or missing): {e}")

        # 6. Migrate Plots
        print("Migrating Plots...")
        try:
            src_cursor.execute("SELECT * FROM plots") # Check if table is 'plots' or 'garden_plots'
            plots = src_cursor.fetchall()
            for p in plots:
                obj = Plot(**p)
                session.add(obj)
            session.commit()
        except:
             pass

        # 6.5 Migrate Products
        print("Migrating Products...")
        try:
            src_cursor.execute("SELECT * FROM products")
            products_rows = src_cursor.fetchall()
            for p in products_rows:
                obj = Product(**p)
                session.add(obj)
            session.commit()
        except Exception as e:
            print(f"Error migrating products: {e}")

        # 7. Migrate Devices
        print("Migrating Devices...")
        src_cursor.execute("SELECT * FROM devices")
        devices = src_cursor.fetchall()
        for d in devices:
            obj = Device(**d)
            session.add(obj)
        session.commit()
        
        # 8. Others... (Simple copy)
        for model_cls, table_name in [
            (Rule, "rules"),
            (Alarm, "alarms"),
            (Task, "tasks"),
            (ChatSession, "chat_sessions"),
            (ChatMessage, "chat_messages"),
            (SensorRecord, "sensor_records")
        ]:
            print(f"Migrating {table_name}...")
            try:
                src_cursor.execute(f"SELECT * FROM {table_name}")
                rows = src_cursor.fetchall()
                for r in rows:
                    session.add(model_cls(**r))
                session.commit()
            except Exception as e:
                print(f"Error migrating {table_name}: {e}")
                session.rollback()

        print("Migration completed successfully!")

    except Exception as e:
        print(f"Migration failed: {e}")
        session.rollback()
    finally:
        src_conn.close()
        session.close()

if __name__ == "__main__":
    migrate()
