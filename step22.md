STEP 22 — BACKEND RELIABILITY AND PRODUCTION-READINESS HARDENING

Goal:
Audit and harden the FastAPI backend now that the complete React → FastAPI → Open-Meteo pipeline is working.

This step is about reliability, resilience, configuration, caching, concurrency, and basic production safety.

IMPORTANT:
Do NOT add authentication.
Do NOT add a database.
Do NOT deploy yet.
Do NOT integrate IMD yet.
Do NOT redesign the frontend.
Do NOT change the personalization engine.
Do NOT introduce a new weather provider.

Make only targeted changes justified by the audit.

==================================================
CURRENT ARCHITECTURE
==================================================

Current flow:

React
 ↓
/api/weather
 ↓
LocationService
 ↓
WeatherService
 ↓
15-minute in-memory cache
 ↓
OpenMeteoWeatherProvider
 ├── Forecast API
 └── Air Quality API

Current development setup:

Frontend: Vite on port 3000
Backend: FastAPI/Uvicorn on port 8000

==================================================
TASK 1 — AUDIT BACKEND STARTUP
==================================================

Inspect:

backend/main.py
backend/requirements.txt

Verify:

- FastAPI app starts cleanly
- routers are registered correctly
- no unnecessary startup work occurs
- no API requests happen during module import
- application can restart cleanly
- health endpoint works immediately after startup

Do not introduce a complex application lifecycle system unless actually necessary.

==================================================
TASK 2 — ENVIRONMENT / CONFIGURATION AUDIT
==================================================

Search the backend for:

- hardcoded production URLs
- API keys
- secrets
- credentials
- localhost assumptions
- debug-only settings
- development-only behavior

Open-Meteo currently does not require an API key for this implementation.

Do NOT create fake environment variables simply for appearance.

If configuration values genuinely belong in environment variables, identify them and make the smallest appropriate change.

Keep local development working.

==================================================
TASK 3 — HTTP CLIENT / CONNECTION BEHAVIOR
==================================================

Inspect the Open-Meteo provider's HTTP implementation.

Verify:

- timeout is enforced
- connections are closed properly
- exceptions are handled cleanly
- malformed provider responses cannot crash the entire application
- concurrent forecast/AQ requests behave correctly

The current implementation uses asyncio.gather.

Verify that:

- forecast failure is handled as the primary weather failure
- AQ failure remains a partial failure
- one failed coroutine does not leave resources hanging

Do not add unnecessary retry loops.

==================================================
TASK 4 — PROVIDER FAILURE TESTING
==================================================

Test at least these scenarios:

1. Normal forecast response
2. Forecast timeout/failure
3. AQ API failure
4. Malformed forecast response
5. Malformed AQ response
6. Location provider failure

Expected behavior:

Forecast failure:
→ clean 502/appropriate upstream error

AQ failure:
→ weather still succeeds
→ AQI/PM values become unavailable

Malformed provider response:
→ clean controlled error
→ no traceback exposed to client

Location failure:
→ clean 503/appropriate service error

Do NOT return fabricated weather.

==================================================
TASK 5 — CACHE AUDIT
==================================================

Inspect the current WeatherService cache.

Verify:

- cache key includes sufficient location identity
- timezone is included
- TTL is exactly 15 minutes
- cache hit avoids provider requests
- expired entries trigger fresh provider requests
- cached_at represents the original cache insertion time
- cache response does not mutate the stored response accidentally

Test:

Request A
→ network

Request A again
→ cache

Wait/force expiration
→ network

Do not change the TTL unless the audit finds a concrete problem.

==================================================
TASK 6 — CACHE MEMORY BEHAVIOR
==================================================

Because the cache is in-memory, inspect whether entries can grow indefinitely.

Determine whether the existing TTL logic actually removes expired entries or merely ignores them.

If expired entries can accumulate indefinitely, implement a small bounded cleanup strategy.

Keep it simple.

Do NOT introduce Redis.
Do NOT introduce a database.
Do NOT introduce an external cache.

A small in-process cleanup mechanism is sufficient for this stage.

==================================================
TASK 7 — CONCURRENT REQUEST AUDIT
==================================================

Test multiple simultaneous requests for:

- same city
- different cities

Verify:

- requests do not corrupt each other's responses
- cache entries remain independent
- timezone does not leak between cities
- one city never receives another city's weather
- application remains responsive

If concurrent identical requests all trigger duplicate upstream requests, document this.

Do NOT implement request coalescing unless there is a clear correctness/performance problem.

==================================================
TASK 8 — INPUT VALIDATION / SECURITY
==================================================

Audit all public backend endpoints.

Verify:

/api/weather
/api/location/search
/api/health

Check:

- excessively long query strings
- whitespace
- empty strings
- unusual characters
- URL encoding
- malformed parameters
- unexpected types

No endpoint should expose Python tracebacks or internal implementation details.

Do not add authentication yet.

Do not add an API gateway.

==================================================
TASK 9 — ERROR RESPONSE CONSISTENCY
==================================================

Inspect HTTP errors from:

- weather API
- location API
- validation failures
- provider failures

Ensure the frontend receives predictable JSON error responses.

Do not expose:

- stack traces
- filesystem paths
- internal Python exception messages
- provider credentials
- raw provider payloads unless intentionally safe

Keep the existing frontend error handling compatible.

==================================================
TASK 10 — CORS AUDIT
==================================================

Inspect the existing CORS configuration.

Current development origins include:

http://localhost:3000
http://127.0.0.1:3000

Verify:

- these continue working
- arbitrary origins are not unnecessarily allowed
- credentials are not enabled unless required

Do NOT configure production domains yet because deployment has not happened.

Document what will need to change during deployment.

==================================================
TASK 11 — RESPONSE CONTRACT AUDIT
==================================================

Verify every /api/weather response is validated through the existing Pydantic WeatherResponse schema.

Test:

- normal response
- AQI unavailable
- optional location fields
- optional marine fields
- empty alerts
- 7 daily entries
- 10 hourly entries

No raw Open-Meteo response should leak directly to the frontend.

==================================================
TASK 12 — TIME / CACHE SEMANTICS
==================================================

Audit:

meta.generatedAt
meta.cachedAt
location.lastUpdated

Ensure these values have distinct meanings.

Rules:

generatedAt:
→ time backend generated/normalized the response

cachedAt:
→ time that response entered the cache

lastUpdated:
→ only a trustworthy provider/model timestamp

Never manufacture a weather observation timestamp from server time.

If a trustworthy provider timestamp is unavailable, keep lastUpdated null.

==================================================
TASK 13 — LOGGING
==================================================

Inspect current backend logging.

Ensure useful operational information can be diagnosed, such as:

- endpoint failure
- provider timeout
- provider failure
- cache miss/hit if already logged

Do NOT log:

- user secrets
- API keys
- unnecessary personal information
- complete raw provider responses

Do not build a complicated logging system.

Use Python's standard logging facilities if logging changes are needed.

==================================================
TASK 14 — HEALTH ENDPOINT
==================================================

Audit /api/health.

It should answer whether the backend process itself is alive.

Do NOT make /api/health dependent on Open-Meteo.

A weather provider outage should not make the process health endpoint falsely appear dead.

If the current implementation already satisfies this, leave it unchanged.

==================================================
TASK 15 — RATE-LIMIT / UPSTREAM CONSIDERATIONS
==================================================

Do NOT implement a complicated rate limiter yet.

Instead inspect whether:

- frontend requests can accidentally loop
- a city change can generate repeated requests
- cache prevents unnecessary provider traffic
- provider calls are bounded by timeout

If a concrete request loop exists, fix it.

Otherwise document rate limiting as a deployment-stage concern.

==================================================
TASK 16 — DEPENDENCY AUDIT
==================================================

Inspect:

backend/requirements.txt

Verify:

- dependencies are actually used
- versions are pinned as currently intended
- no unnecessary packages were added
- httpx remains compatible with the implementation

Do not upgrade dependencies simply because newer versions exist.

Do not perform a broad dependency upgrade.

==================================================
TASK 17 — PERFORMANCE SMOKE TEST
==================================================

Run a simple backend smoke test.

Measure/observe:

- cold weather request
- cached weather request
- several different cities
- concurrent requests

Exact latency numbers are not important.

We care about:

- correctness
- no crashes
- cache effectiveness
- no cross-city contamination

==================================================
TASK 18 — REGRESSION TESTS
==================================================

Verify:

GET /api/health

GET /api/location/search?query=Jaipur

GET /api/location/search?query=London

GET /api/weather?location=Jaipur

GET /api/weather?location=Mumbai

GET /api/weather?location=London

Also verify the frontend still builds.

Do not modify frontend code unless a backend contract regression genuinely requires it.

==================================================
TASK 19 — PRODUCTION READINESS CHECKLIST
==================================================

After the audit, classify each item:

READY
NEEDS DEPLOYMENT CONFIGURATION
NEEDS FUTURE WORK

Check:

- startup
- configuration
- HTTP timeouts
- provider failure handling
- AQ degradation
- cache
- cache memory behavior
- concurrency
- input validation
- error responses
- CORS
- response schema
- timestamp semantics
- logging
- health endpoint
- dependency hygiene
- frontend compatibility

Do not claim something is production-ready if it still depends on local development assumptions.

==================================================
IMPORTANT BOUNDARIES
==================================================

DO NOT:

- add authentication
- add database
- add Redis
- add IMD
- add tides
- add official alerts
- add another provider
- deploy
- redesign frontend
- modify personalizationEngine.js
- change personalization logic
- delete mockWeather.js
- change the 15-minute cache TTL without evidence
- add unnecessary dependencies
- perform broad refactoring

If the system is already correct in an area, leave it unchanged.

==================================================
MANDATORY REPORTING
==================================================

After implementation, report:

1. Exact files created
2. Exact files modified
3. Exact files deleted
4. Backend startup result
5. Configuration/security findings
6. HTTP client audit result
7. Forecast failure test
8. AQ failure test
9. Malformed response test
10. Location failure test
11. Cache hit test
12. Cache expiry test
13. Cache memory behavior
14. Concurrent same-city test
15. Concurrent different-city test
16. Input validation test
17. Error response audit
18. CORS audit
19. Pydantic response validation result
20. Timestamp semantics result
21. Logging result
22. Health endpoint result
23. Rate-limit/request-loop findings
24. Dependency audit
25. Performance smoke-test result
26. Full endpoint regression result
27. Frontend build result
28. Every code change and why
29. Remaining production blockers
30. Items deferred to deployment
31. Assumptions
32. Deviations from this prompt

IMPORTANT:
If you discover an issue that requires a larger architectural change, DO NOT implement that larger change in this step. Report it clearly.

Then STOP.

Do not proceed to Step 23.