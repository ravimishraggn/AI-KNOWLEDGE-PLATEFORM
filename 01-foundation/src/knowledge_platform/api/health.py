"""
Platform health check endpoints.
These are always available and do not require authentication.
"""
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live", summary="Liveness probe")
async def liveness() -> dict:
    """Returns 200 if the process is running. Used by Kubernetes liveness probe."""
    return {"status": "alive"}


@router.get("/ready", summary="Readiness probe")
async def readiness() -> dict:
    """
    Returns 200 if the platform is ready to serve traffic.
    Checks: database connection, Redis connection, plugin registry loaded.
    Not implemented yet — placeholder.
    """
    return {"status": "ready", "checks": {}}


@router.get("/startup", summary="Startup probe")
async def startup() -> dict:
    """Returns 200 when platform initialization is complete."""
    return {"status": "started"}
