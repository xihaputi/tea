import sqlite3

# Connect to the database
db_path = "d:/thingsboard_envor/tea/backend/tea_garden.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Add sensor_config column to devices table
    cursor.execute("ALTER TABLE devices ADD COLUMN sensor_config TEXT")
    print("Successfully added 'sensor_config' column to 'devices' table.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("Column 'sensor_config' already exists.")
    else:
        print(f"Error adding column: {e}")

conn.commit()
conn.close()
