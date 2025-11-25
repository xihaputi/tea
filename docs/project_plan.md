# Project Plan (high level)

1) MVP (week 1)
- Stand up FastAPI with core routes: plots, sensor, advice, disease upload.
- Ship uni-app pages: index, plot detail, disease upload.
- Use mock data + rule-based advice; Swagger available at `/docs`.

2) Integrations (week 2-3)
- Swap mock data for DB (SQLite → MySQL), wire SQLAlchemy CRUD.
- Add real disease model inference; optimize upload path.
- Hook LLM/ASR (iFlyTek) via `llm_client.py` / `speech_client.py`.

3) Polish (week 4)
- Add charts (history, stats), chat UI polish, risk map.
- Containerize backend; add CI lint/test; write deployment docs.
