
STEP 15 — BUILD THE LOCATION RESOLUTION SERVICE CONTRACT

We have approved the Step 14 backend contract.

Now build ONLY the location-resolution layer.

Do NOT integrate a real geocoding provider yet.

Do NOT integrate Open-Meteo.

Do NOT integrate IMD.

Do NOT modify the React frontend.

Do NOT add authentication, database, user accounts, or backend personalization.

Do NOT modify the existing /api/weather behavior yet.

OBJECTIVE

Create a clean backend location service that establishes the contract:

user-entered location
        ↓
location service
        ↓
canonical location information

The actual external geocoding provider will be connected in a later step.

TASK 1 — INSPECT THE CURRENT CODE

Review:

backend/main.py
backend/api/
backend/services/
backend/schemas/
backend/data/
src/data/mockWeather.js
the current onboarding location input
and any existing frontend location handling.

Understand how the current application represents a user's entered location.

Do not modify frontend code.

TASK 2 — CREATE A NORMALIZED LOCATION MODEL

Create an appropriate Pydantic model under:

backend/schemas/

The normalized location result should be able to represent at minimum:

- city
- state/region
- country
- latitude
- longitude
- timezone
- displayName

Use appropriate optional/nullable typing where real geocoding data may not provide a field.

Do not add unnecessary fields such as postal code, street address, building number, etc.

We only need city-level weather for this product at this stage.

TASK 3 — CREATE A LOCATION SERVICE ABSTRACTION

Create a small service abstraction under:

backend/services/

The service should conceptually support:

resolve_location(query)

Do NOT call any external provider yet.

The important goal is that the API layer should not know how geocoding is implemented.

Keep the design simple.

Do NOT create a large framework or plugin system.

TASK 4 — CREATE A LOCATION API ENDPOINT

Add:

GET /api/location/search?query=Jaipur

For this step, use a small deterministic internal mock dataset or stub implementation.

The purpose is to prove the API contract, NOT to provide real geocoding.

The endpoint should return a predictable normalized location result.

For example, a Jaipur query may resolve to:

{
  "city": "Jaipur",
  "state": "Rajasthan",
  "country": "India",
  "latitude": 26.9124,
  "longitude": 75.7873,
  "timezone": "Asia/Kolkata",
  "displayName": "Jaipur, Rajasthan, India"
}

The exact JSON structure should follow the Pydantic model you create.

TASK 5 — QUERY VALIDATION

Validate the query parameter.

It should:

- be required
- reject empty input
- reject whitespace-only input
- have a reasonable maximum length

Use predictable HTTP errors.

Do not implement fuzzy search or ranking yet.

TASK 6 — UNKNOWN LOCATION

Define clear behavior for a location that the mock resolver does not know.

For example:

GET /api/location/search?query=SomeUnknownPlace

should return an appropriate 4xx response rather than fabricating coordinates.

Choose a sensible status code and explain the choice in the report.

TASK 7 — DO NOT CONNECT WEATHER YET

The location endpoint is independent from /api/weather.

Do NOT modify /api/weather to use this service yet.

Do NOT make weather calls based on coordinates yet.

That will happen after the real location provider is established.

TASK 8 — KEEP PROVIDER ABSTRACTION READY

The architecture should allow a future implementation such as:

LocationService
      ↓
GeocodingProvider
      ↓
Nominatim / another provider

But for this step, use only the deterministic mock/stub implementation.

Do not create unnecessary provider classes unless they are genuinely useful for keeping the service boundary clean.

TASK 9 — TEST

Verify:

1. GET /api/location/search?query=Jaipur
2. GET /api/location/search?query=Mumbai
3. GET /api/location/search?query=Bengaluru
4. GET /api/location/search without query
5. GET /api/location/search?query=
6. GET /api/location/search?query=%20%20%20
7. GET /api/location/search?query=SomeUnknownPlace
8. GET /api/health
9. GET /api/weather?location=Jaipur

Confirm the existing endpoints still work.

Also run the frontend production build.

IMPORTANT

Do not change:

- Dashboard.jsx
- mockWeather.js
- personalizationEngine.js
- onboarding UI
- existing weather response structure

The frontend must remain exactly as it is.

REPORTING REQUIREMENT — MANDATORY

When finished, STOP and report:

1. Exact files created
2. Exact files modified
3. Final location model
4. Location API endpoint and response shape
5. Location service architecture
6. Mock/stub locations supported
7. Unknown-location behavior and status code
8. Validation behavior and status codes
9. Results of every requested endpoint test
10. Whether /api/health still passes
11. Whether /api/weather still passes
12. Whether frontend files remained untouched
13. Whether frontend production build passes
14. Any assumptions or issues
15. Any deviations from these instructions

Do not integrate a real geocoder.
Do not proceed to the next step.
STOP after the report.