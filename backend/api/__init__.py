"""
API Routers for Mausam Backend.
"""

from backend.api.health import router as health_router
from backend.api.weather import router as weather_router
from backend.api.location import router as location_router

__all__ = ["health_router", "weather_router", "location_router"]
