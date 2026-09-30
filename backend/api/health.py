"""
Health router — GET /api/health

Returns a minimal JSON object confirming the backend is running.
"""

from datetime import datetime, timezone
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Liveness check — no dependencies exercised."""
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "mausam-backend",
    }
