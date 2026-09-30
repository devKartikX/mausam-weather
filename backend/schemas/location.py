"""
Normalized Location Schema for Mausam (Step 15).

Defines the stable canonical location contract returned by the location resolution service.
"""

from typing import Optional
from pydantic import BaseModel, Field


class LocationResult(BaseModel):
    city: str = Field(..., description="Canonical city or locality name", examples=["Jaipur"])
    state: Optional[str] = Field(None, description="State, province, or region", examples=["Rajasthan"])
    country: str = Field(..., description="Country name", examples=["India"])
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Latitude coordinate", examples=[26.9124])
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Longitude coordinate", examples=[75.7873])
    timezone: Optional[str] = Field(None, description="IANA timezone identifier", examples=["Asia/Kolkata"])
    displayName: str = Field(..., description="Formatted full location display string", examples=["Jaipur, Rajasthan, India"])
