"""
Mausam Backend — FastAPI application entry point (Step 15)

Startup:
    cd /Users/kartikgupta/Desktop/SIH
    uvicorn backend.main:app --reload --port 8000

Interactive docs: http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.health import router as health_router
from backend.api.weather import router as weather_router
from backend.api.location import router as location_router
from backend.api.diagnostics import router as diagnostics_router

app = FastAPI(
    title="Mausam Backend API",
    description=(
        "Backend service for the Mausam personalized weather application. "
        "Phase 2 — Step 15: location resolution service contract."
    ),
    version="0.2.0",
)

import os

# ---------------------------------------------------------------------------
# CORS Configuration
# Defaults to local Vite development server.
# In production, set FRONTEND_URL or ALLOWED_ORIGINS environment variable
# to the deployed HTTPS origin (e.g. https://mausam-frontend.onrender.com).
# Wildcard (*) is intentionally rejected to ensure production security.
# ---------------------------------------------------------------------------
DEFAULT_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

env_frontend = os.getenv("FRONTEND_URL", "").strip()
env_allowed = os.getenv("ALLOWED_ORIGINS", "").strip()

active_origins = list(DEFAULT_ORIGINS)
if env_frontend:
    for url in env_frontend.split(","):
        cleaned = url.strip().rstrip("/")
        if cleaned and cleaned not in active_origins:
            active_origins.append(cleaned)

if env_allowed:
    for url in env_allowed.split(","):
        cleaned = url.strip().rstrip("/")
        if cleaned and cleaned not in active_origins:
            active_origins.append(cleaned)

app.add_middleware(
    CORSMiddleware,
    allow_origins=active_origins,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(health_router, prefix="/api", tags=["health"])
app.include_router(weather_router, prefix="/api", tags=["weather"])
app.include_router(location_router, prefix="/api", tags=["location"])
app.include_router(diagnostics_router, prefix="/api", tags=["diagnostics"])
