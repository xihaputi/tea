# API Spec (draft)

Base URL: `http://localhost:8000`

## Plots
- `GET /plots` → list plots.
- `POST /plots` → create plot (name, location, status?).
- `GET /plots/{id}` → get plot.

## Sensor
- `GET /sensor/latest?plot_id=1` → latest record.
- `GET /sensor/history?plot_id=1&period=7d` → mock history list.

## Advice
- `GET /advice/today?plot_id=1` → moisture-based advice.

## Disease
- `POST /disease/detect` (form-data file) → mock prediction + saved path.

## Chat
- `POST /chat/ask` → stub LLM response.

## Stats
- `GET /stats/summary?plot_id=1` → aggregate snapshot.

