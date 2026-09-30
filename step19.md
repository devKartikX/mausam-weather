STEP 19 — IMPLEMENT REAL WEATHER SERVICE

Step 18 analysis is approved.

Now implement the first real weather-data pipeline.

IMPORTANT SCOPE

Implement ONLY:

LocationResult
    ↓
WeatherService
    ↓
Open-Meteo Forecast API + Air Quality API
    ↓
normalized WeatherResponse
    ↓
GET /api/weather?location=...

Do NOT modify the React frontend yet.

Do NOT create weatherClient.js.

Do NOT modify Dashboard.jsx.

Do NOT remove src/data/mockWeather.js.

Do NOT connect personalization to the backend.

Do NOT integrate IMD.

Do NOT implement authentication or database.

Marine integration should remain minimal and optional in this step.

==================================================
TASK 1 — CREATE WEATHER PROVIDER
==================================================

Create:

backend/services/providers/open_meteo_weather.py

Implement a small provider responsible for calling the Open-Meteo Forecast API.

Use:

https://api.open-meteo.com/v1/forecast

The provider should accept:

- latitude
- longitude
- timezone

from LocationResult.

Request only the variables actually required by our normalized contract.

Forecast requirements:

CURRENT / NEAR-CURRENT:
- temperature_2m
- relative_humidity_2m
- apparent_temperature
- weather_code
- wind_speed_10m
- wind_direction_10m
- visibility
- uv_index

HOURLY:
- temperature_2m
- weather_code
- precipitation_probability

DAILY:
- temperature_2m_max
- temperature_2m_min
- precipitation_probability_max
- weather_code
- sunrise
- sunset

Use:

temperature_unit=celsius
wind_speed_unit=kmh
precipitation_unit=mm
timezone=<resolved location timezone>

Request 7 forecast days.

IMPORTANT:

Do NOT request current.precipitation_probability unless the API documentation explicitly supports it for the current endpoint at implementation time.

For current rain probability, use an explicitly documented hourly probability value according to a clear rule.

Document the rule in code.

==================================================
TASK 2 — AIR QUALITY
==================================================

Also call:

https://air-quality-api.open-meteo.com/v1/air-quality

Request only:

- us_aqi
- pm2_5
- pm10

Use the resolved latitude/longitude and location timezone where appropriate.

IMPORTANT:

The normalized `aqi` field represents:

US AQI

Do NOT call it:
- Indian AQI
- CPCB AQI
- National AQI

unless a real CPCB/Indian AQI source is later integrated.

Derive:

aqiStatus:

0–50:
"Good"

51–100:
"Moderate"

101–150:
"Unhealthy for Sensitive Groups"

151–200:
"Unhealthy"

201–300:
"Very Unhealthy"

301+:
"Hazardous"

If AQI data is unavailable, use null.

Do not make air-quality failure cause the entire weather request to fail.

==================================================
TASK 3 — LOCATION RESOLUTION
==================================================

Update /api/weather so it no longer uses the static Jaipur mock weather response.

Flow must become:

GET /api/weather?location=Mumbai

        ↓

LocationService.resolve_location("Mumbai")

        ↓

LocationResult

        ↓

WeatherService

        ↓

Open-Meteo Forecast + Air Quality

        ↓

WeatherResponse

The weather response must use the resolved location:

- city
- state
- country
- latitude
- longitude
- timezone

Do not hardcode Jaipur anywhere in the live weather path.

==================================================
TASK 4 — WEATHER CODE MAPPING
==================================================

Create a dedicated mapping utility under an appropriate backend module.

Map WMO weather codes to:

- condition
- frontend icon identifier

Use the mapping established in Step 18.

Cover:

0
1
2
3
45
48
51
53
55
61
63
65
71
73
75
77
80
81
82
85
86
95
96
99

Also provide a safe fallback for unexpected codes.

Never return an undefined icon.

==================================================
TASK 5 — WIND DIRECTION
==================================================

Convert wind direction degrees to 16-point compass directions:

N
NNE
NE
ENE
E
ESE
SE
SSE
S
SSW
SW
WSW
W
WNW
NW
NNW

Use a deterministic conversion.

==================================================
TASK 6 — TIMEZONE AND TIME FORMATTING
==================================================

All weather timestamps must use the resolved LocationResult.timezone.

Do NOT use:
- server timezone
- developer machine timezone
- browser timezone

Hourly:

Return a reasonable set of upcoming hourly entries required by the existing frontend.

The current frontend needs enough entries to support its hourly horizontal scroller.

For the first live implementation, return the next 10 hours.

The first/current entry should be labeled:

"Now"

Subsequent entries should be local 12-hour labels such as:

"7 PM"
"8 PM"
"9 PM"

Daily:

Return exactly 7 days.

Day 0:

"Today"

Then use local abbreviated weekday names:

"Thu"
"Fri"
etc.

Sunrise/sunset:

Format into the frontend-compatible local display strings:

"06:14 AM"

Do not append fabricated freshness text.

==================================================
TASK 7 — CURRENT HIGH/LOW
==================================================

Populate:

current.highTemp
current.lowTemp

from:

daily.temperature_2m_max[0]
daily.temperature_2m_min[0]

Do not derive these from hourly data.

==================================================
TASK 8 — VISIBILITY
==================================================

Open-Meteo visibility is returned in meters.

Convert to kilometers.

Example:

8000 → 8.0

Keep the normalized API field:

visibility

in kilometers.

==================================================
TASK 9 — UV STATUS
==================================================

Derive:

uvStatus

using:

0–2:
"Low"

3–5:
"Moderate"

6–7:
"High"

8–10:
"Very High"

11+:
"Extreme"

If this differs from existing frontend assumptions, preserve the normalized backend semantics and report it.

==================================================
TASK 10 — MARINE DATA
==================================================

Do NOT build a complex MarineProvider yet.

For this step:

- keep waveHeight nullable
- keep seaSurfaceTemp nullable
- keep tidalInfo null

Do NOT fabricate marine data.

If implementing waveHeight is trivial without complicating WeatherService, it may be added, but it is NOT required for this step.

Tidal data must remain null.

==================================================
TASK 11 — ALERTS
==================================================

For real Open-Meteo weather mode:

alerts = []

Do NOT convert rain, heat, wind, or other normal forecast conditions into an "alert".

Do NOT claim official IMD warnings.

Official alerts will be a future provider integration.

==================================================
TASK 12 — META
==================================================

For live weather:

meta.source = "open-meteo"

meta.isDemo = false

meta.locationQuery = original user query

generatedAt = actual backend response-generation timestamp in UTC

cachedAt = cache timestamp when applicable

Do not use:

"Just now"

as a freshness claim.

==================================================
TASK 13 — ELEVATION / LOCATION METADATA
==================================================

Populate location.elevation from the weather provider if available.

If unavailable:

null

Do not fabricate elevation.

Keep:

location.lastUpdated

nullable.

If a trustworthy provider observation/model timestamp is available, populate it.

Otherwise:

null

Do NOT write "Updated just now".

==================================================
TASK 14 — CACHING
==================================================

Implement WeatherService caching.

Use:

15-minute TTL

Cache key should include at least:

rounded latitude
rounded longitude
timezone

Example conceptual key:

26.920:75.788:Asia/Kolkata

Cache successful normalized weather responses only.

Keep cache in memory.

Do NOT introduce Redis or a database.

Ensure cache hits do not call Open-Meteo again.

==================================================
TASK 15 — TIMEOUTS
==================================================

Use a reasonable outbound timeout.

Target:

5 seconds

Do not allow requests to hang indefinitely.

==================================================
TASK 16 — FAILURE HANDLING
==================================================

Weather provider failures:

- timeout
- connection failure
- HTTP 5xx
- malformed response

must NOT produce fake live weather.

If the forecast provider fails:

return HTTP 502 or 503 with a clean message.

If Forecast succeeds but Air Quality fails:

return weather with:

aqi = null
aqiStatus = null
pm25 = null
pm10 = null

and continue successfully.

Do not fail the entire weather request because AQI failed.

If malformed forecast data prevents a valid WeatherResponse:

return a clean 502.

Do not expose raw upstream error bodies.

==================================================
TASK 17 — PROVIDER ABSTRACTION
==================================================

Keep a minimal abstraction so WeatherService does not depend on raw HTTP details.

Conceptually:

WeatherProvider
    ↓
OpenMeteoWeatherProvider

Do not create a huge plugin framework.

==================================================
TASK 18 — TEST REAL WEATHER
==================================================

Test:

1. Jaipur
2. Mumbai
3. Bengaluru
4. Kolkata
5. Delhi
6. Chennai
7. London

For each, verify:

- HTTP 200
- correct resolved city
- country
- latitude
- longitude
- timezone
- real current temperature
- humidity
- wind
- visibility
- UV
- high/low
- hourly forecast
- 7-day forecast
- alerts = []
- AQI if available

IMPORTANT:

Do NOT compare values against the old mock data.

The whole purpose is now to obtain real location-specific values.

==================================================
TASK 19 — CITY DIFFERENTIATION TEST
==================================================

This is critical.

Explicitly verify that at least:

Jaipur
Mumbai
London

produce different real weather/location results.

This prevents accidentally retaining hardcoded mock Jaipur data.

==================================================
TASK 20 — CACHE TEST
==================================================

Demonstrate:

first request:
network call

second identical request:
cache hit

third equivalent request after location normalization:
same cache key where applicable

Confirm provider call count does not increase on cache hit.

==================================================
TASK 21 — REGRESSION
==================================================

Verify:

GET /api/health

still works.

Verify:

GET /api/location/search?query=Jaipur

still works.

Verify frontend production build still passes.

DO NOT MODIFY FRONTEND FILES.

==================================================
IMPORTANT FINAL CONSTRAINTS
==================================================

Do NOT:

- modify Dashboard.jsx
- create weatherClient.js
- remove mockWeather.js
- integrate IMD
- implement marine tides
- implement official alerts
- implement authentication
- implement database
- implement personalization backend
- change frontend UI
- expose Open-Meteo raw JSON

This step is ONLY the backend real-weather pipeline.

==================================================
REPORTING REQUIREMENT — MANDATORY
==================================================

When finished, STOP and report:

1. Exact files created
2. Exact files modified
3. Dependencies added
4. Final backend architecture
5. Forecast API URL and parameters
6. Air Quality API URL and parameters
7. WeatherResponse mapping
8. WMO mapping implementation
9. Wind direction implementation
10. Timezone handling
11. Hourly data handling
12. Daily data handling
13. AQI semantics
14. Marine behavior
15. Alert behavior
16. Cache implementation
17. Cache TTL
18. Timeout
19. Error handling
20. Jaipur real-weather result
21. Mumbai real-weather result
22. Bengaluru result
23. Kolkata result
24. Delhi result
25. Chennai result
26. London result
27. City differentiation verification
28. Cache verification
29. /api/health regression
30. /api/location regression
31. Frontend build result
32. Any assumptions/issues
33. Any deviations

Do not proceed to frontend migration.
STOP after the report.