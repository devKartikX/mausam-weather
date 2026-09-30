STEP 18 — ANALYZE REAL WEATHER PROVIDER AND NORMALIZED WEATHER MAPPING

IMPORTANT:
THIS IS AN ANALYSIS-ONLY STEP.

Do NOT modify any files.
Do NOT install dependencies.
Do NOT implement the weather provider.
Do NOT modify the frontend.
Do NOT modify /api/weather.
Do NOT remove mockWeather.js.

We have successfully implemented real location resolution in Step 17.

We now have:

LocationResult
- city
- state
- country
- latitude
- longitude
- timezone
- displayName

The next objective is to determine exactly how real weather data should be obtained and mapped into our existing normalized WeatherResponse.

CURRENT ARCHITECTURE

User location
    ↓
/api/location/search
    ↓
LocationService
    ↓
OpenMeteoGeocodingProvider
    ↓
LocationResult
    ↓
latitude + longitude + timezone
    ↓
future WeatherService
    ↓
normalized WeatherResponse

DO NOT IMPLEMENT ANYTHING YET.

TASK 1 — INSPECT CURRENT CONTRACT

Review:

backend/schemas/weather.py
backend/data/mock_weather.py
backend/api/weather.py
src/data/mockWeather.js
all current dashboard weather consumers
personalizationEngine.js

Document exactly which weather fields the frontend currently consumes.

Do not invent fields.

TASK 2 — RESEARCH OPEN-METEO WEATHER API

Use current official Open-Meteo documentation.

Investigate the generic forecast API:

https://api.open-meteo.com/v1/forecast

Determine which parameters/variables can provide:

CURRENT:

- temperature
- apparent/feels-like temperature
- relative humidity
- precipitation probability
- wind speed
- wind direction
- visibility
- weather condition/code
- UV index
- sunrise
- sunset

HOURLY:

- temperature
- condition/weather code
- precipitation probability
- other fields required by the current frontend

DAILY:

- maximum temperature
- minimum temperature
- precipitation probability
- weather condition/code
- sunrise
- sunset if useful

TASK 3 — WEATHER CODE MAPPING

Determine how Open-Meteo WMO weather codes should map to our current:

condition
icon

Do NOT assume the frontend can directly consume Open-Meteo weather codes.

Design a small backend mapping layer such as:

WMO code
    ↓
normalized condition
    ↓
frontend-compatible icon identifier

Identify the complete mapping needed for the codes likely to appear.

TASK 4 — TIMEZONE

Determine how to request weather data using the timezone returned by LocationResult.

The normalized weather response must use local location time for:

- hourly timestamps
- daily dates/day labels
- sunrise
- sunset

Do not use server timezone.

Do not use browser timezone.

The requested city's timezone must control weather timestamps.

TASK 5 — AIR QUALITY

Investigate the current official Open-Meteo Air Quality API.

Determine whether it can provide:

- PM2.5
- PM10
- AQI

Determine what AQI definition/scale is returned.

This is important because our current UI says "AQI" and displays a status.

Do NOT assume the API's AQI scale matches the current mock AQI semantics.

Determine whether:

- we can safely map the provider AQI directly
- we need to specify a particular AQI variable/scale
- the current frontend label/status needs adjustment
- or the field should temporarily be nullable

TASK 6 — MARINE / BEACH & SURF DATA

Investigate the current official Open-Meteo Marine API.

Determine whether it provides:

- wave height
- sea surface temperature
- wave direction
- wave period
- swell information
- tides

Compare those capabilities with our current fields:

- waveHeight
- seaSurfaceTemp
- tidalInfo

Do NOT fabricate tidal data.

If tides are unavailable, explicitly recommend null/unavailable behavior.

Also determine how we should distinguish:

- inland location
- coastal location
- marine data unavailable

TASK 7 — ALERTS / WARNINGS

This is important.

Our current WeatherResponse contains:

alerts[]

But Open-Meteo's normal forecast response is not equivalent to an official government weather-warning feed.

Determine whether the chosen weather provider can supply official alerts/warnings.

Do NOT represent generic weather conditions as official warnings.

If official alerts are unavailable, recommend how alerts should behave:

- empty list
- separate advisory source later
- another provider later

Explicitly identify this gap.

TASK 8 — AGRICULTURE / PERSONALIZATION DATA

Review the existing personalization engine.

Determine which real weather fields already available from the weather provider are sufficient for:

- Health
- Fitness
- Travel
- Commuting
- Family
- Agriculture
- Events
- Beach & Surf

Identify any personalization fields that cannot be reliably populated from the selected provider.

Do NOT invent new environmental data just to satisfy a card.

TASK 9 — PROVIDER STRATEGY

Evaluate whether we should initially use:

Open-Meteo Weather API
+
Open-Meteo Air Quality API
+
Open-Meteo Marine API

or whether another provider is required for any specific capability.

Do not assume one provider must provide everything.

Consider the architecture:

WeatherService
    ├── WeatherProvider
    ├── AirQualityProvider
    └── MarineProvider
             ↓
      Normalized WeatherResponse

Determine whether this is justified or whether a simpler architecture is sufficient for the first implementation.

Avoid over-engineering.

TASK 10 — CACHING

Recommend appropriate backend caching for weather data.

Unlike location data, weather changes frequently.

Determine:

- suggested cache TTL
- whether current/hourly/daily data should share TTL
- whether one complete normalized response can be cached
- how cache keys should incorporate:
  - latitude
  - longitude
  - timezone
  - relevant query options

Keep this simple for the first implementation.

No Redis/database yet.

TASK 11 — FAILURE BEHAVIOR

Design behavior for:

- weather provider timeout
- provider 4xx
- provider 5xx
- malformed response
- air-quality unavailable
- marine unavailable
- location resolved but weather unavailable

The backend must never silently turn provider failures into fake weather.

Determine whether we should return:

- 502
- 503
- partial response with nullable fields

and explain why.

TASK 12 — CURRENT NORMALIZED CONTRACT REVIEW

Compare the current WeatherResponse schema against the real provider capabilities.

Produce a table:

| Current field | Real source | Available? | Mapping | Nullable? | Notes |

Include EVERY field in:

meta
location
current
hourly
daily
alerts

Do not skip fields.

TASK 13 — IMPORTANT: IDENTIFY CONTRACT CHANGES

If the existing WeatherResponse contains fields that cannot be reliably populated by real APIs, identify them.

Do NOT change the schema yet.

Recommend exactly what should happen:

- keep required
- make nullable
- remove
- derive
- provide through another provider

TASK 14 — REALISTIC MVP

Design the smallest real-weather MVP that gives us:

- real current temperature
- feels-like temperature
- humidity
- wind
- precipitation probability
- visibility
- UV
- sunrise/sunset
- real hourly forecast
- real 7-day forecast
- real AQI if reliably available

while keeping unsupported data honest.

TASK 15 — IMD CONSIDERATION

We ultimately want Mausam to be credible as an Indian weather product.

Investigate the current official IMD API availability/documentation at a high level.

Do NOT integrate IMD.

Determine:

- whether official APIs are publicly accessible
- what registration/authentication appears necessary
- whether real-time observations/forecasts/warnings are available
- whether IMD should be treated as a future official-data provider

Clearly separate verified facts from assumptions.

REPORTING REQUIREMENT — MANDATORY

When finished, STOP and report:

1. Exact current frontend weather fields consumed
2. Open-Meteo forecast variables selected
3. WMO weather-code mapping strategy
4. Timezone strategy
5. Air-quality capabilities
6. AQI scale/semantics
7. Marine capabilities
8. Tide limitations
9. Alert/warning limitations
10. Personalization field coverage
11. Recommended provider architecture
12. Recommended caching strategy
13. Failure-handling strategy
14. Complete field-by-field WeatherResponse mapping table
15. Fields requiring contract changes
16. Recommended real-weather MVP
17. IMD findings
18. Verified facts vs engineering assessment vs assumptions
19. Proposed Step 19 implementation plan
20. Any unresolved questions

DO NOT WRITE CODE.
DO NOT MODIFY FILES.
DO NOT INSTALL DEPENDENCIES.
STOP AFTER THE ANALYSIS.