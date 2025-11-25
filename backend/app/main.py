from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import advice, chat, disease, plots, sensor, stats


def create_app() -> FastAPI:
    """Application factory to allow reuse in tests or scripts."""
    app = FastAPI(title="Digital Tea Garden API", version="0.1.0")

    # Basic CORS setup for local dev; tighten this in production.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(plots.router)
    app.include_router(sensor.router)
    app.include_router(advice.router)
    app.include_router(disease.router)
    app.include_router(chat.router)
    app.include_router(stats.router)
    return app


app = create_app()

