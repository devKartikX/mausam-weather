STEP 14 — VERIFY AND HARDEN THE BACKEND API CONTRACT

Do NOT integrate any real weather provider.

Do NOT add geocoding.

Do NOT modify the React frontend.

Do NOT add authentication, database, user accounts, or personalization migration.

The goal of this step is to inspect and lightly harden the backend created in Step 13 so that it is ready for a real weather provider later.

IMPORTANT:
Keep this step small and reversible.

TASK 1 — INSPECT THE CURRENT BACKEND

Review:

backend/main.py
backend/api/health.py
backend/api/weather.py
backend/data/mock_weather.py
backend/schemas/
backend/services/

Also inspect the existing frontend weather consumers and src/data/mockWeather.js to ensure the backend contract remains compatible with the frontend's existing data needs.

Do not change frontend code.

TASK 2 — IDENTIFY THE CURRENT CONTRACT

Document the exact current response structure of:

GET /api/weather?location=Jaipur

Identify:

- required fields
- optional fields
- nullable fields
- arrays
- nested structures
- fields that are currently demo/mock metadata
- fields that may eventually come from different providers

TASK 3 — INTRODUCE PYDANTIC RESPONSE MODELS

If the current implementation does not already use Pydantic response models, introduce minimal Pydantic models under:

backend/schemas/

Create models representing the normalized weather contract.

Keep them focused.

Do NOT create models for provider-specific responses.

The API should return the normalized contract, not an Open-Meteo/IMD-specific structure.

Use appropriate optional/nullable typing where a real provider may legitimately not have a value.

For example, marine fields must be able to represent unavailable data without inventing values.

TASK 4 — USE RESPONSE MODELS IN THE API

Update the weather endpoint to use the appropriate FastAPI response model.

Do not change the external JSON structure unnecessarily.

Backward compatibility with the Step 13 response is important.

TASK 5 — VALIDATE INPUT

Keep:

GET /api/weather?location=Jaipur

The location query parameter should:

- be required
- reject an empty/whitespace-only value
- have a sensible maximum length
- return a clear HTTP 4xx response for invalid input

Do not implement sophisticated location validation yet.

TASK 6 — HEALTH ENDPOINT

Keep /api/health working.

Do not add unnecessary health-check complexity.

The current response can remain:

{
  "status": "ok",
  "timestamp": "...",
  "service": "mausam-backend"
}

TASK 7 — ERROR HANDLING

Add only minimal API-level error handling where appropriate.

Do not build a large exception framework.

The goal is predictable HTTP behavior, not production observability yet.

TASK 8 — TEST THE CONTRACT

Run and verify:

1. GET /api/health
2. GET /api/weather?location=Jaipur
3. GET /api/weather without location
4. GET /api/weather?location=
5. GET /api/weather?location=<reasonable valid city>

Confirm status codes and JSON responses.

Also confirm:

- backend starts cleanly
- frontend build still passes
- no frontend files were modified

IMPORTANT ARCHITECTURE CONSTRAINT

Do NOT create a WeatherProvider implementation yet.

Do NOT create OpenMeteoProvider yet.

Do NOT create IMDProvider yet.

Do NOT call any external API.

We are only stabilizing the normalized contract.

REPORTING REQUIREMENT — MANDATORY

When finished, STOP and report:

1. Exact files created
2. Exact files modified
3. Final backend folder structure
4. Final normalized weather response schema
5. Which fields are required
6. Which fields are nullable/optional
7. Validation behavior and status codes
8. Health endpoint result
9. Weather endpoint result
10. Invalid-input test results
11. Whether frontend files remained untouched
12. Whether frontend production build passes
13. Any assumptions or issues
14. Any deviations from these instructions

Do not proceed to the next step.
STOP after the report.