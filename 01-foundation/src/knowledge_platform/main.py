"""
FastAPI application factory for the Knowledge Operating Platform.
Business logic is implemented in individual plane packages.
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config.settings import PlatformSettings
from .api.health import router as health_router


def create_app(settings: PlatformSettings | None = None) -> FastAPI:
    """
    Create and configure the FastAPI application.

    This factory is the single entry point for the platform application.
    Planes register their routers by calling app.include_router() after
    the app is created.
    """
    if settings is None:
        settings = PlatformSettings()

    app = FastAPI(
        title="Knowledge Operating Platform",
        description="Enterprise Knowledge Operating System API",
        version="0.1.0",
        docs_url="/docs" if settings.enable_docs else None,
        redoc_url="/redoc" if settings.enable_docs else None,
    )

    # Middleware (order matters — outermost first)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Platform routers
    app.include_router(health_router)

    return app
