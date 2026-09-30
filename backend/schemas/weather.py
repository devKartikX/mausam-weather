"""
Normalized Weather Response Schemas for Mausam (Step 14).

Defines the stable, provider-agnostic data contract for the Mausam backend API.
Compatible with frontend data expectations while accommodating real weather providers
and nullable fields (e.g. marine data for inland regions, air quality, optional alerts).
"""

from typing import List, Optional, Union
from pydantic import BaseModel, Field


class TidalInfo(BaseModel):
    highTide: Optional[str] = Field(None, description="Time of high tide, e.g. '10:45 AM'")
    lowTide: Optional[str] = Field(None, description="Time of low tide, e.g. '04:30 PM'")


class LocationSchema(BaseModel):
    city: str = Field(..., description="City or locality name")
    state: Optional[str] = Field(None, description="State or administrative region")
    country: str = Field(..., description="Country name")
    latitude: Optional[float] = Field(None, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, description="Longitude coordinate")
    timezone: Optional[str] = Field(None, description="IANA timezone name, e.g. 'Asia/Kolkata'")
    elevation: Optional[Union[float, int, str]] = Field(None, description="Elevation above sea level")
    lastUpdated: Optional[str] = Field(None, description="Human readable or ISO last updated stamp")


class CurrentWeatherSchema(BaseModel):
    temp: float = Field(..., description="Current temperature in Celsius")
    condition: str = Field(..., description="Weather condition description")
    feelsLike: float = Field(..., description="Feels-like temperature in Celsius")
    highTemp: float = Field(..., description="Daily high temperature in Celsius")
    lowTemp: float = Field(..., description="Daily low temperature in Celsius")
    humidity: int = Field(..., ge=0, le=100, description="Relative humidity percentage")
    windSpeed: float = Field(..., ge=0, description="Wind speed in km/h")
    windDirection: str = Field(..., description="Wind direction compass heading, e.g. 'NW'")
    rainProbability: int = Field(..., ge=0, le=100, description="Precipitation probability percentage")
    visibility: float = Field(..., ge=0, description="Visibility in kilometers")
    uvIndex: float = Field(..., ge=0, description="UV Index value")
    uvStatus: str = Field(..., description="UV Index category (e.g. 'Low', 'Moderate', 'High', 'Very High')")
    aqi: Optional[int] = Field(None, ge=0, description="Air Quality Index")
    aqiStatus: Optional[str] = Field(None, description="AQI category (e.g. 'Good', 'Moderate', 'Poor')")
    pm25: Optional[float] = Field(None, ge=0, description="PM2.5 particulate concentration")
    pm10: Optional[float] = Field(None, ge=0, description="PM10 particulate concentration")
    sunrise: str = Field(..., description="Sunrise time string")
    sunset: str = Field(..., description="Sunset time string")
    icon: str = Field(..., description="Icon identifier code (e.g. 'Sun', 'CloudSun', 'CloudRain')")
    # Marine / Coastal fields (nullable for inland locations)
    waveHeight: Optional[float] = Field(None, description="Wave height in meters")
    seaSurfaceTemp: Optional[float] = Field(None, description="Sea surface temperature in Celsius")
    tidalInfo: Optional[TidalInfo] = Field(None, description="Tidal information if coastal")


class HourlyForecastSchema(BaseModel):
    time: str = Field(..., description="Hour label, e.g. 'Now', '8 PM'")
    temp: float = Field(..., description="Forecasted temperature in Celsius")
    condition: str = Field(..., description="Forecasted condition description")
    pop: int = Field(..., ge=0, le=100, description="Probability of precipitation percentage")
    icon: str = Field(..., description="Icon identifier code")


class DailyForecastSchema(BaseModel):
    day: str = Field(..., description="Day label, e.g. 'Today', 'Wed'")
    condition: str = Field(..., description="Forecasted condition description")
    high: float = Field(..., description="Day high temperature in Celsius")
    low: float = Field(..., description="Day low temperature in Celsius")
    pop: int = Field(..., ge=0, le=100, description="Probability of precipitation percentage")
    icon: str = Field(..., description="Icon identifier code")


class WeatherAlertSchema(BaseModel):
    id: str = Field(..., description="Unique alert identifier")
    level: str = Field(..., description="Alert severity level, e.g. 'advisory', 'warning', 'severe'")
    badge: str = Field(..., description="Display badge text")
    title: str = Field(..., description="Alert title")
    time: str = Field(..., description="Timing or validity window")
    description: str = Field(..., description="Detailed alert description")


class WeatherMetaSchema(BaseModel):
    source: str = Field(..., description="Data source identifier, e.g. 'mock', 'open-meteo'")
    generatedAt: str = Field(..., description="Timestamp when response was generated (ISO 8601)")
    cachedAt: Optional[str] = Field(None, description="Timestamp when data was cached (ISO 8601)")
    locationQuery: str = Field(..., description="The query string used to request the weather")
    isDemo: bool = Field(False, description="Flag indicating mock/demo data")
    isStale: bool = Field(False, description="Flag indicating whether data is served from stale cache fallback")
    staleReason: Optional[str] = Field(None, description="Reason why stale data was returned")
    dataAgeSeconds: Optional[int] = Field(None, description="Age of data in seconds since provider generation")
    alertsAvailable: bool = Field(True, description="Whether the alerts service was reachable")


class WeatherResponse(BaseModel):
    meta: WeatherMetaSchema = Field(..., description="Metadata regarding provider and timeliness")
    location: LocationSchema = Field(..., description="Geographical location details")
    current: CurrentWeatherSchema = Field(..., description="Current weather observations")
    hourly: List[HourlyForecastSchema] = Field(..., description="Hourly forecast array")
    daily: List[DailyForecastSchema] = Field(..., description="Daily forecast array")
    alerts: List[WeatherAlertSchema] = Field(default_factory=list, description="Active weather alerts")
