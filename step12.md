ANALYZE ONLY — Phase 2 Backend Architecture & Live Weather Migration

IMPORTANT:
This is an ANALYSIS task only.

Do NOT create, modify, delete, rename, or move any files.
Do NOT install dependencies.
Do NOT change the frontend.
Do NOT change mock data.
Do NOT create the backend yet.

We are beginning Phase 2 of the Mausam project:
migrate the current polished React prototype from mock weather data toward a real, deployable weather system.

The current frontend is already working and must be treated as the reference implementation.

==================================================
PROJECT GOAL
==================================================

Eventually we want:

User
 ↓
React Frontend
 ↓
FastAPI Backend
 ↓
Location Service
 ↓
Weather Service
 ↓
Official IMD provider where available
 + fallback weather provider where necessary
 ↓
Normalized weather response
 ↓
Personalization Engine
 ↓
Personalized Dashboard

Later we may add:
- database
- persistent user preferences
- authentication
- deployment

Do NOT implement any of these yet.

==================================================
PART 1 — INSPECT CURRENT FRONTEND
==================================================

Inspect the existing repository carefully.

Identify:

1. Current frontend framework/build setup.
2. Current application entry point.
3. Current onboarding state structure.
4. How name, location, and selected interests are currently stored.
5. How Dashboard receives user data.
6. How weather data currently enters the dashboard.
7. Exact file containing mock weather data.
8. Exact structure/schema of the current mock weather object.
9. Every component that depends directly or indirectly on mockWeather.
10. Current personalizationEngine inputs and outputs.
11. Whether any component assumes Jaipur-specific data.
12. Whether any component assumes the weather data is always immediately available.
13. Existing loading/error/fallback behavior.
14. Existing services/utilities that could be reused.

Do not modify anything.

==================================================
PART 2 — TRACE THE DATA FLOW
==================================================

Document the current data flow precisely:

Onboarding
→ user preferences
→ App
→ Dashboard
→ weather data
→ weather components
→ personalization engine
→ personalized cards

Show which files are involved at every stage.

Explicitly identify the point where we should eventually introduce:

Frontend
→ API client
→ FastAPI

==================================================
PART 3 — DESIGN THE WEATHER CONTRACT
==================================================

Using the EXISTING mockWeather structure as the starting point, propose a normalized backend weather response.

Do NOT redesign the frontend yet.

Identify:

A. Existing fields that can remain unchanged.

B. Existing fields that should become dynamic.

C. Fields that need metadata.

D. Fields currently mocked but that may not be available from every provider.

E. Fields needed by the existing 8 personalization categories.

The proposed normalized response should conceptually cover:

location
current weather
hourly forecast
daily forecast
alerts
air quality
marine data where available
metadata/source
updated timestamp
timezone

Do not invent provider-specific values.

==================================================
PART 4 — LOCATION ARCHITECTURE
==================================================

Design how:

"Jaipur"

or

"Mumbai"

will become a normalized location object containing, where available:

- city/name
- state/region
- country
- latitude
- longitude
- timezone

Explain:

- where geocoding should happen
- whether frontend or backend should own it
- how ambiguous/unknown cities should be handled
- how location errors should be returned

The frontend should eventually send a user location query to our backend rather than directly depending on a third-party geocoder.

==================================================
PART 5 — WEATHER PROVIDER ARCHITECTURE
==================================================

Research/consider the current project requirements and propose a provider abstraction.

Desired conceptual structure:

WeatherService
├── IMDProvider
└── FallbackProvider

Explain:

1. What should belong to the provider adapter.
2. What should belong to the common WeatherService.
3. How provider-specific responses should be normalized.
4. How provider failure should be handled.
5. How the frontend should remain provider-agnostic.
6. Which weather fields are critical to the existing UI.
7. Which fields may require a secondary provider.

Do NOT implement providers.

==================================================
PART 6 — IMD INTEGRATION REQUIREMENTS
==================================================

Investigate the existing project context and determine what we need to know before integrating IMD.

Identify:

- API access requirements
- authentication/API key requirements if applicable
- endpoint categories relevant to our application
- location/input requirements
- forecast/observation/warning data availability
- rate limits or access restrictions if documented
- caching requirements if documented
- deployment/IP considerations if documented

Clearly distinguish:

FACTS VERIFIED FROM CURRENT OFFICIAL DOCUMENTATION

from:

ASSUMPTIONS / THINGS WE STILL NEED TO VERIFY

Do not claim an IMD endpoint works unless it has actually been verified.

==================================================
PART 7 — FALLBACK PROVIDER
==================================================

Evaluate whether a fallback provider such as Open-Meteo can cover the fields required by our current UI and personalization engine.

Do not implement it.

Identify:

- current weather support
- hourly support
- daily support
- precipitation probability
- humidity
- wind
- visibility
- UV
- sunrise/sunset
- air quality
- timezone
- limitations
- attribution/licensing considerations

Again, distinguish verified facts from assumptions.

==================================================
PART 8 — PERSONALIZATION MIGRATION
==================================================

Current state:

React
→ personalizationEngine.js

Eventually:

Backend
→ personalization service

Analyze whether the existing personalization engine should:

A. remain temporarily on frontend,

B. be duplicated in backend during migration,

or

C. be moved immediately.

Recommend the safest migration approach.

We want to avoid breaking the currently working UI.

Identify exactly what inputs the personalization engine requires from live weather data.

==================================================
PART 9 — PROPOSED API CONTRACT
==================================================

Propose the minimum backend endpoints we will eventually need.

At this stage focus only on weather/location infrastructure.

For example, consider:

GET /api/health

GET /api/location/search?query=...

GET /api/weather?city=...

Do not implement them.

For each endpoint provide:

- purpose
- request
- response shape
- success behavior
- invalid input behavior
- provider failure behavior

Do not add authentication endpoints yet.

==================================================
PART 10 — MIGRATION STRATEGY
==================================================

Design a safe migration from:

mockWeather.js

to:

backend live weather API

We specifically want a transitional architecture that allows:

Mock Provider
and
Live Provider

to coexist temporarily.

Explain how to prevent a backend migration from breaking the existing UI.

Identify the smallest first implementation milestone.

==================================================
PART 11 — RISKS
==================================================

Identify likely risks:

- CORS
- API keys
- provider access
- rate limits
- city ambiguity
- timezone
- missing weather fields
- provider outages
- stale data
- API latency
- marine data availability
- AQI availability
- frontend assumptions
- deployment issues

For each, propose a mitigation.

==================================================
PART 12 — PROPOSED IMPLEMENTATION ORDER
==================================================

Give us an ordered sequence of small implementation steps.

Example structure:

Step 13 — Backend skeleton
Step 14 — Health endpoint
Step 15 — Location service
Step 16 — Weather provider abstraction
Step 17 — Fallback weather provider
Step 18 — Normalized weather response
Step 19 — Frontend API client
Step 20 — Mock/live switching
...

Do NOT implement these steps.

We will execute them one at a time after reviewing your analysis.

==================================================
IMPORTANT RULES
==================================================

- Analysis only.
- Zero code changes.
- Zero file changes.
- Zero dependency installation.
- Do not create backend files.
- Do not alter mockWeather.js.
- Do not alter personalizationEngine.js.
- Do not alter React components.
- Do not make assumptions without clearly labeling them.
- Preserve the existing frontend as the reference implementation.
- Prefer the smallest safe migration path.

==================================================
REPORT BACK
==================================================

Provide:

1. CURRENT ARCHITECTURE
2. CURRENT DATA FLOW
3. CURRENT WEATHER DATA CONTRACT
4. PERSONALIZATION INPUT/OUTPUT ANALYSIS
5. PROPOSED NORMALIZED WEATHER CONTRACT
6. LOCATION ARCHITECTURE
7. WEATHER PROVIDER ARCHITECTURE
8. IMD REQUIREMENTS
9. FALLBACK PROVIDER ANALYSIS
10. PROPOSED API CONTRACT
11. MIGRATION STRATEGY
12. RISKS + MITIGATIONS
13. ORDERED IMPLEMENTATION PLAN
14. FIRST IMPLEMENTATION MILESTONE
15. FILES CHANGED

For item 15, it MUST say:

"None — analysis only."

STOP HERE.
Do not implement anything.