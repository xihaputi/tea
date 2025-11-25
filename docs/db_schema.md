# DB Schema (draft)

Core tables (SQLAlchemy models in `backend/app/models.py`):

- `garden_plots`: id, name, location, status.
- `sensor_records`: id, plot_id → garden_plots.id, soil_moisture, temperature, humidity, timestamp.
- `advice_records`: id, plot_id, soil_moisture, level, advice, timestamp.
- `disease_records`: id, plot_id (nullable), image_path, disease_type, confidence, advice, timestamp.

Dev DB: SQLite at `data/tea.db` (configurable). Prod: MySQL/MariaDB with matching schema.
