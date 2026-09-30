STEP 20 — CONNECT FRONTEND TO REAL WEATHER BACKEND

Goal:
Replace the frontend's direct dependency on mock weather data with the existing FastAPI /api/weather endpoint.

IMPORTANT:
This is an implementation task.
Do NOT redesign the UI.
Do NOT modify the personalization engine.
Do NOT add authentication, database, or deployment work.
Do NOT change the backend unless absolutely required to fix a frontend integration contract issue.
Keep this step small and reversible.

CURRENT BACKEND CONTRACT:

GET /api/weather?location={query}

The backend now returns the normalized WeatherResponse containing:

meta
location
current
hourly
daily
alerts

The backend is already live and tested with real Open-Meteo data.

TASK 1 — CREATE FRONTEND WEATHER CLIENT

Create a small dedicated frontend service, for example:

src/services/weatherClient.js

Responsibilities:

- Call the backend:
  /api/weather?location={encodedLocation}

- Use fetch or the existing frontend HTTP approach if one already exists.
- Do NOT call Open-Meteo directly from React.
- Do NOT expose provider APIs or keys in frontend code.
- Parse the JSON response.
- If response.ok is false, throw a useful error containing the backend status/message.
- Handle network failure cleanly.
- Keep the client focused only on HTTP communication.

Do not put UI logic inside weatherClient.js.

TASK 2 — CONNECT DASHBOARD WEATHER DATA

Find the existing code path where the dashboard currently obtains weather from:

src/data/mockWeather.js

Replace that data source with the new weather client.

The user's selected/onboarded city must become the location query sent to:

/api/weather?location={city}

Use the existing persisted onboarding/preferences data rather than introducing a new city state system.

Do not duplicate the user's city in another storage location.

TASK 3 — PRESERVE THE EXISTING UI CONTRACT

The existing Dashboard and personalization components were built around the normalized weather shape.

Before modifying components, inspect how the current mockWeather object is consumed.

Prefer adapting the API response at ONE boundary if necessary rather than scattering API-specific transformations throughout the UI.

The dashboard should continue receiving the same logical fields it already expects:

location
current temperature
condition
feelsLike
highTemp
lowTemp
humidity
windSpeed
windDirection
rainProbability
visibility
uvIndex / uvStatus
aqi / aqiStatus
pm25
pm10
sunrise
sunset
icon
hourly
daily
alerts
marine fields where available

Do NOT rewrite the personalization engine.

TASK 4 — LOADING STATE

Add a proper loading state while the real backend request is in progress.

Use the existing application's visual language.

Do not redesign the dashboard.

The loading state should prevent the dashboard from briefly rendering stale/mock weather while the real request is loading.

TASK 5 — ERROR STATE

If the backend request fails:

- Do not silently fall back to mockWeather.
- Do not show fake weather.
- Show a clear user-friendly error state.
- Preserve the user's selected city.
- Provide a retry mechanism if the current UI architecture makes this straightforward.

Do not expose raw stack traces or technical backend details to the user.

TASK 6 — REMOVE MOCK WEATHER DEPENDENCY

After successful integration:

- Dashboard runtime must no longer import/use mockWeather.js.
- Do NOT immediately delete mockWeather.js.
- Leave the file untouched for now as a rollback/reference asset.
- Verify there are no remaining runtime imports of mockWeather.js from the dashboard weather path.

TASK 7 — PERSONALIZATION SAFETY

The personalization engine must continue receiving the same normalized weather information.

Do NOT modify:

src/services/personalizationEngine.js

Do NOT change:
- interest categories
- card priority logic
- scoring
- recommendation rules

This step is ONLY about changing the weather data source.

TASK 8 — API URL / DEVELOPMENT SETUP

Inspect the existing Vite development configuration.

Use the cleanest existing mechanism for reaching the FastAPI backend.

Prefer a Vite development proxy if the project architecture already supports it, so frontend code can call:

/api/weather

instead of hardcoding:

http://127.0.0.1:8000

If a proxy is required, make the smallest possible Vite configuration change.

Do not introduce environment-variable complexity unless genuinely necessary.

Do NOT hardcode production URLs.

TASK 9 — VERIFY REAL DATA

Run the frontend and backend together.

Test at least:

Jaipur
Mumbai
Bengaluru
Delhi
London

Verify that changing the selected city results in a backend request for that city and the dashboard displays differentiated real weather.

Specifically verify:

- temperature changes
- condition changes when applicable
- humidity/wind values update
- AQI updates
- hourly data updates
- daily forecast updates
- location name updates
- timezone-sensitive times remain correct

TASK 10 — VERIFY PERSONALIZATION

Test at least two different interest profiles using real weather.

Confirm that personalization still works exactly as before.

Do NOT evaluate or redesign the recommendation quality in this step.

TASK 11 — VERIFY ERROR BEHAVIOR

Test at least one failure scenario, such as:

- backend stopped/unavailable
- invalid location if reachable through the existing onboarding flow

Confirm:

- no mock weather appears
- loading state ends
- useful error UI appears
- app does not crash

TASK 12 — BUILD + REGRESSION

Run:

- frontend production build
- backend health check
- backend weather endpoint
- frontend integration test/manual verification

Confirm there are no new console errors.

IMPORTANT BOUNDARIES:

DO NOT:
- modify personalizationEngine.js
- add authentication
- add database
- add user accounts
- integrate IMD
- integrate tides
- integrate official alerts
- redesign Dashboard UI
- redesign onboarding
- change interest categories
- delete mockWeather.js
- add direct Open-Meteo calls to frontend
- add new weather providers
- implement deployment

The objective is simply:

CURRENT:
React → mockWeather.js

TARGET:
React → weatherClient → FastAPI /api/weather → LocationService → WeatherService → Open-Meteo

MANDATORY REPORTING:

After implementation, report:

1. Exact files created
2. Exact files modified
3. Exact files deleted, if any
4. How the frontend calls /api/weather
5. How the selected city is obtained
6. Whether a Vite proxy was added/used
7. How API errors are handled
8. How loading state is handled
9. How mockWeather was removed from the runtime path
10. Whether personalizationEngine.js was modified
11. Any response-shape adapter/transformations added
12. Jaipur test result
13. Mumbai test result
14. Bengaluru test result
15. Delhi test result
16. London test result
17. Personalization regression result
18. Backend failure/error-state result
19. Frontend console result
20. Production build result
21. Any assumptions
22. Any deviations from these instructions
23. Any issues still requiring attention

Then STOP.

Do not proceed to Step 21.