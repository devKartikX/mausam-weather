STEP 17 — IMPLEMENT THE REAL OPEN-METEO GEOCODING PROVIDER

Step 16 analysis has been approved.

Now implement ONLY the real geocoding integration.

OBJECTIVE

Replace the deterministic mock resolver inside LocationService with a real Open-Meteo Geocoding provider while preserving the existing API contract:

GET /api/location/search?query=...

→ LocationResult

Do NOT integrate weather yet.

Do NOT modify the React frontend.

Do NOT modify /api/weather.

Do NOT add authentication.

Do NOT add a database.

Do NOT implement personalization on the backend.

Do NOT implement autocomplete.

IMPORTANT PROVIDER RULE

Open-Meteo's free API is appropriate for our current development/SIH non-commercial phase.

Do not claim it is automatically suitable for future commercial production.

Keep the provider abstraction so we can replace it later.

ARCHITECTURE

Implement:

GET /api/location/search
        ↓
LocationService
        ↓
GeocodingProvider abstraction
        ↓
OpenMeteoGeocodingProvider
        ↓
Open-Meteo Geocoding API
        ↓
LocationResult

TASK 1 — DEPENDENCY

Add the minimum HTTP client dependency required for backend-to-backend API requests.

Prefer async HTTP using httpx.

Do not add unnecessary dependencies.

Update backend/requirements.txt.

TASK 2 — PROVIDER INTERFACE

Create a minimal provider abstraction under backend/services/ or an appropriate provider module.

The abstraction should expose the capability needed by LocationService, conceptually:

resolve(query) -> LocationResult | None

Keep it small.

Do NOT create a large generic plugin framework.

TASK 3 — OPEN-METEO PROVIDER

Implement an Open-Meteo geocoding provider.

Use the official endpoint:

https://geocoding-api.open-meteo.com/v1/search

Use the `name` query parameter.

Request only the number of results we actually need.

The current application does not implement a location-selection UI, so initially select the best/first suitable result returned by the provider.

Do not expose the Open-Meteo response directly to the frontend.

TASK 4 — MAPPING

Map the provider response into our existing LocationResult:

Open-Meteo:
name       → city
admin1     → state
country    → country
latitude   → latitude
longitude  → longitude
timezone   → timezone

Build:

displayName

using the available city/state/country values.

Do NOT invent missing state/timezone values.

If timezone is absent, preserve it as null.

Do NOT use a country-based hardcoded timezone fallback.

TASK 5 — LOCATION SERVICE

Update LocationService so that it uses the provider.

The service should:

1. normalize the incoming query
2. check cache
3. call OpenMeteoGeocodingProvider on cache miss
4. normalize the result
5. cache successful results
6. return LocationResult

Keep the existing internal canonical/mock dictionary only as a graceful fallback for a small set of known demo cities if the external provider is unavailable.

IMPORTANT:

The fallback must NOT fabricate locations for unknown queries.

If:

- Open-Meteo fails
- AND query is not in the known fallback dictionary

return an appropriate service-unavailable error.

If Open-Meteo returns zero results for a valid query, return the existing 404 behavior.

TASK 6 — CACHE

Implement a simple in-memory cache.

Requirements:

- normalized cache key: `query.strip().lower()`
- TTL: 24 hours initially
- cache only successful location resolutions
- no need for persistent storage
- keep implementation simple

Do not add Redis or a database.

TASK 7 — TIMEOUT

Use a reasonable outbound HTTP timeout.

Target approximately 4 seconds.

Do not allow an external geocoding request to hang indefinitely.

TASK 8 — ERROR HANDLING

Handle at least:

1. successful response
2. zero results
3. HTTP 4xx from provider
4. HTTP 5xx from provider
5. timeout
6. connection/network failure
7. malformed/unexpected provider response

Rules:

- zero results → HTTP 404
- provider unavailable/network failure:
  - try known internal fallback dictionary
  - if fallback has no entry → HTTP 503
- never fabricate coordinates
- never return an empty successful LocationResult

Do not leak raw provider error payloads to the client.

TASK 9 — SECURITY / PRIVACY

No API key is required for the current Open-Meteo free non-commercial endpoint.

Do not add a fake API key.

Do not expose provider internals unnecessarily.

Only send the user's location query required for geocoding.

Do not log unnecessary personal information.

TASK 10 — PROVIDER ATTRIBUTION

The application will eventually need appropriate attribution for Open-Meteo/location data.

For this step, do not redesign the frontend.

Add a concise code comment or backend documentation note explaining that Open-Meteo/GeoNames attribution must be included in the eventual user-facing product.

Do not falsely claim that attribution has already been added to the UI.

TASK 11 — TEST REAL GEOCODING

Test at minimum:

1. Jaipur
2. Mumbai
3. Bengaluru
4. Kolkata
5. Delhi
6. Chennai
7. a global city such as London
8. an unknown location
9. whitespace-only input
10. missing query

For at least Jaipur and Mumbai, verify that:

- city is sensible
- country is correct
- latitude is in valid range
- longitude is in valid range
- timezone is populated when provider supplies it

Do not require exact coordinates to equal our old mock coordinates. The real provider may return a nearby canonical coordinate.

TASK 12 — TEST CACHE

Demonstrate that:

- first lookup causes provider resolution
- repeated normalized lookup uses cache
- e.g. `Jaipur`, `jaipur`, and ` Jaipur ` map to the same cache key

Do not make unnecessary external requests.

TASK 13 — REGRESSION TEST

Confirm:

GET /api/health

still works.

Confirm:

GET /api/weather?location=Jaipur

still works exactly as before.

Do NOT connect /api/weather to the newly resolved location yet.

The weather migration is a separate future step.

Confirm frontend production build still passes.

IMPORTANT — DO NOT DO THESE

Do NOT:

- modify Dashboard.jsx
- modify onboarding UI
- create weatherClient.js
- integrate Open-Meteo weather API
- integrate IMD
- modify personalizationEngine.js
- add authentication
- add database
- add Redis
- implement autocomplete
- redesign the frontend
- remove the mock weather system

This step is ONLY real geocoding.

REPORTING REQUIREMENT — MANDATORY

When finished, STOP and report:

1. Exact files created
2. Exact files modified
3. Dependencies added
4. Final provider architecture
5. Open-Meteo endpoint used
6. Exact mapping into LocationResult
7. Cache implementation and TTL
8. Timeout configuration
9. Error-handling behavior
10. Fallback behavior
11. Result for Jaipur
12. Result for Mumbai
13. Result for Bengaluru
14. Result for Kolkata
15. Result for Delhi
16. Result for Chennai
17. Result for London
18. Unknown-location result
19. Invalid-input results
20. Cache verification result
21. /api/health regression result
22. /api/weather regression result
23. Frontend build result
24. Any assumptions/issues
25. Any deviations

Do not proceed to weather integration.
STOP after the report.