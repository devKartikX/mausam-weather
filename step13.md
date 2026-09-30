STEP 13 — IMPLEMENT ONLY THE FASTAPI BACKEND SKELETON

We have completed the architecture analysis.

Now implement ONLY the backend foundation needed to establish:

React → weatherClient → FastAPI → mock weather response

Do NOT integrate any real weather provider yet.
Do NOT implement geocoding yet.
Do NOT implement authentication, database, user accounts, or backend personalization.
Do NOT migrate personalizationEngine.js.
Do NOT redesign the frontend.

OBJECTIVE

Create a minimal FastAPI backend that can run independently and expose a basic health endpoint plus a temporary mock weather endpoint.

The purpose of this step is ONLY to prove that the frontend can eventually communicate with a backend safely.

IMPLEMENTATION REQUIREMENTS

1. Inspect the existing repository structure before making changes.

2. Create a clean backend structure appropriate for the existing React/Vite project.

Prefer a structure similar to:

backend/
  main.py
  api/
  services/
  schemas/
  data/

Keep it minimal. Do not create unnecessary layers or files.

3. Create the FastAPI application.

The backend must:
- start successfully with uvicorn
- expose GET /api/health
- return a small JSON response indicating the backend is healthy

Example shape is acceptable:

{
  "status": "ok"
}

4. Add CORS configuration for local development.

Allow the existing Vite development origin used by this project.

Do not use a wildcard "*" if a specific localhost origin can be configured cleanly.

If the frontend currently runs on port 3000, support that origin.

5. Create a temporary mock weather endpoint:

GET /api/weather

For this step it may return a static mock response.

However, DO NOT invent a completely new weather schema.

Inspect the existing src/data/mockWeather.js first and design the response so that it can eventually represent the existing frontend weather data without forcing unnecessary frontend rewrites.

The endpoint should accept a location parameter in a simple form, for example:

GET /api/weather?location=Jaipur

The location parameter does not need to influence the mock values yet.

6. Keep the backend response JSON serializable and predictable.

7. Add basic error handling for missing/invalid location input if appropriate, but do not over-engineer validation yet.

8. Add only the dependencies actually required for the FastAPI backend.

If the repository already has a suitable Python environment or dependency setup, reuse it rather than creating unnecessary environment machinery.

9. Do NOT modify Dashboard.jsx yet.

Do NOT create weatherClient.js yet.

Do NOT remove mockWeather.js.

The existing frontend must continue to work exactly as before.

10. Do not integrate:
- Open-Meteo
- Nominatim
- IMD
- external APIs
- API keys
- database
- authentication

Those belong to later steps.

11. Verify the backend independently.

Run:
- backend startup
- GET /api/health
- GET /api/weather?location=Jaipur

Confirm that each returns valid JSON.

12. Verify the existing frontend still builds successfully.

IMPORTANT ARCHITECTURE RULE

The backend mock response should be designed as a future normalized weather contract rather than a provider-specific response.

Do not expose Open-Meteo-specific field names or provider-specific structures.

REPORTING REQUIREMENT — MANDATORY

When finished, STOP and report:

1. Exact files created
2. Exact files modified
3. Backend folder structure
4. Exact API endpoints created
5. Example JSON response from /api/health
6. Example JSON response from /api/weather?location=Jaipur
7. How CORS was configured
8. Dependencies added
9. Commands used to run the backend
10. Whether the frontend build still passes
11. Any assumptions or issues
12. Any deviations from these instructions

Do not proceed to the next step.
Do not implement anything beyond this task.
STOP after the report.