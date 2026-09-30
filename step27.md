STEP 27 — COMPLETE REMAINING PRODUCT REQUIREMENTS + FINAL BACKEND DATA HARDENING

Goal:

The core Mausam application is now working end-to-end:

React frontend
→ FastAPI backend
→ real Open-Meteo weather
→ location autocomplete
→ canonical location/timezone
→ personalization
→ city switching
→ corrected timezone/greeting/hourly forecast behavior.

The next objective is to resolve the remaining product/data requirements in one controlled implementation pass BEFORE the final UI/UX polish and deployment.

This is a consolidated task.

IMPORTANT:
Work carefully and inspect the existing repository before modifying anything.

Do NOT break any functionality that has already been verified.

==================================================
CURRENT VERIFIED FOUNDATION
==================================================

Already working:

- React + Vite frontend
- FastAPI backend
- normalized WeatherResponse
- Open-Meteo weather provider
- Open-Meteo geocoding
- multi-result location autocomplete
- canonical location object
- localStorage persistence
- city switching
- timezone-aware greetings
- timezone-aware hourly forecast
- backend caching
- frontend/backend error handling
- personalization engine
- responsive baseline
- accessibility baseline

Do NOT redesign or replace these systems.

==================================================
PART A — AQI: LOCK THE CORRECT SEMANTICS
==================================================

CURRENT STATE:

The application currently uses Open-Meteo Air Quality data and displays:

"Air Quality (US EPA)"

This must remain factually accurate.

IMPORTANT:

Do NOT implement a homemade CPCB/NAQI score from only the current PM2.5/PM10 values.

Do NOT label US AQI as:
- Indian AQI
- CPCB AQI
- NAQI

Do NOT change the existing US EPA AQI calculation unless a clear bug is found.

Open-Meteo's AQI documentation defines US AQI using pollutant-specific averaging periods.

Therefore:

1. Keep the existing US EPA AQI implementation.
2. Keep the UI label explicitly:
   "Air Quality (US EPA)"
3. Keep the existing AQI category semantics.
4. Verify that the displayed category matches the actual US AQI value.
5. Verify null/unavailable AQI is handled safely.
6. Ensure personalization cards do not claim CPCB/Indian AQI.
7. Add a small source/semantics label where appropriate if the current UI makes the standard ambiguous.

CPCB/NAQI is FUTURE SCOPE.

Do not implement CPCB AQI in this task.

==================================================
PART B — OFFICIAL IMD WEATHER ALERTS
==================================================

This is the most important remaining India-specific requirement.

Research the currently accessible official IMD warning sources before coding.

Potential official sources include:

- IMD API Management Platform
- IMD district-wise warning interfaces
- IMD CAP alert infrastructure / official CAP feeds
- WMO/WIS metadata for IMD CAP alerts

IMPORTANT:

Do NOT assume an API endpoint works just because it appears in old documentation.

Before implementation:

1. Verify which official source is currently accessible without private credentials.
2. Verify its current response format.
3. Verify whether it contains:
   - location/district
   - warning type
   - warning severity/color
   - issue time
   - validity/date
   - description where available

3. Prefer an official structured source over HTML scraping.
4. Do NOT use browser scraping if a structured official feed/API is available.
5. Do NOT hardcode fake alerts.
6. Do NOT create mock severe-weather warnings and present them as real.

Architecture:

Create an isolated AlertsService / IMDAlertsProvider.

Do NOT put IMD-specific logic inside:
- WeatherService
- OpenMeteoWeatherProvider
- React components

Target architecture:

FastAPI
   |
   +-- WeatherService
   |      |
   |      +-- OpenMeteoWeatherProvider
   |
   +-- AlertsService
          |
          +-- IMDAlertsProvider

The base weather response must continue working even if the IMD alert provider fails.

Alerts are additive.

==================================================
PART C — ALERT CONTRACT
==================================================

Inspect the existing WeatherAlert schema.

Do not break the existing frontend contract.

Map official IMD warnings into the existing normalized alert structure.

At minimum preserve:

- severity/level
- title
- description
- issued/valid time if supported
- source
- warning type
- location/district where supported

Use official IMD severity semantics where available.

Do NOT arbitrarily reinterpret warning colors.

If IMD provides:

Green / Yellow / Orange / Red

preserve those semantics in the normalized model.

If no active official warning exists:

alerts = []

This is a valid successful response.

If alert provider fails:

base weather must still return successfully.

Do NOT convert provider failure into a fake "No alerts" state internally.

The system should distinguish:

- provider successfully checked and no alerts
- provider unavailable

Do not silently hide provider failures during backend diagnostics.

==================================================
PART D — LOCATION → IMD DISTRICT MAPPING
==================================================

This is a major architectural issue.

The selected canonical location currently contains:

- city
- state
- country
- latitude
- longitude
- timezone

It may NOT contain a district identifier.

Do NOT pretend city == district.

For Indian alerts:

1. Determine whether the selected location can be mapped reliably to an IMD district.
2. Prefer an authoritative/maintainable mapping.
3. If reliable mapping is unavailable for a location, do not fabricate an alert match.
4. Return no matched alert for that location rather than showing another district's warning.

For the MVP, it is acceptable to support a documented subset of locations if this limitation is explicit and safely handled.

Do NOT map "Jaipur" to a district simply because the names happen to match without verification.

==================================================
PART E — ALERT CACHING
==================================================

Do NOT reuse the normal 15-minute weather cache blindly for emergency warnings.

Implement an independent alert cache strategy.

Recommended:

- short TTL
- bounded memory
- no stale-alert serving
- provider failures do not reuse expired warnings as active warnings

IMPORTANT:

Never serve stale official warnings as if they are current.

If the alert source is unavailable:

- weather may still be returned
- alert data should be treated as unavailable rather than current

==================================================
PART F — MARINE / BEACH & SURF
==================================================

Implement Marine support only where appropriate.

Use Open-Meteo Marine API through a backend provider.

Do NOT call the Marine API directly from React.

Architecture:

WeatherService
    |
    +-- OpenMeteoWeatherProvider
    |
    +-- OpenMeteoMarineProvider

Marine data should be optional.

For inland locations:

- marine fields remain null
- no fake wave/tide values
- Beach & Surf personalization must gracefully indicate that marine conditions are not applicable

For coastal locations, where the marine provider has valid data, support:

- wave height
- wave direction if useful
- wave period
- sea surface temperature

Do NOT present modeled sea-level height as a precise astronomical tide table.

If sea_level_height_msl is used:

label it accurately as modeled sea level / sea level height.

Do not call it:

"Next high tide"

unless an authoritative tide prediction source actually provides high/low tide events.

Open-Meteo explicitly warns that its modeled sea-level/tide information has limited coastal accuracy and is not suitable for navigation.

Therefore:

- use marine data for lifestyle/surf context
- do not present it as navigational information

If marine provider fails:

- base weather remains successful
- marine fields become null
- no fabricated values

==================================================
PART G — COASTAL DETECTION
==================================================

Do not create a crude rule such as:

"latitude < X = coastal"

Do not hardcode cities such as:

Mumbai = coastal
Jaipur = inland

unless this is only a test fixture.

Prefer a provider-supported/coordinate-based strategy.

If reliable automatic coastal detection is difficult, it is acceptable to query marine data only for selected Beach & Surf profiles or use a bounded supported-location strategy.

Do not cause marine requests for every inland weather request if avoidable.

==================================================
PART H — STALE WEATHER FALLBACK
==================================================

Implement a safe stale-weather fallback.

Current behavior:

provider failure → error

New behavior:

If a fresh weather request fails AND a recently expired weather cache entry exists:

return the cached weather with explicit metadata:

isStale: true

and a meaningful stale timestamp/age.

Example UI meaning:

"Weather data may be outdated"
"Updated 28 minutes ago"

IMPORTANT:

Do NOT claim the data is current.

Do NOT use stale cache for:

- official IMD alerts
- emergency warnings
- active warning status

Stale fallback applies only to normal weather telemetry/forecast where appropriate.

Recommended maximum stale age:

60 minutes.

If cached weather is older than the maximum stale window:

return the normal provider error.

Do not make the stale window configurable through frontend input.

==================================================
PART I — WEATHER RESPONSE METADATA
==================================================

Inspect the existing meta schema.

If necessary, add backward-compatible metadata fields:

- isStale
- staleReason
- dataAgeSeconds or equivalent

Do not break existing clients.

Do not fabricate timestamps.

Keep:

generatedAt
cachedAt
lastUpdated

semantically distinct.

==================================================
PART J — CACHE HARDENING
==================================================

Preserve the existing bounded in-memory caches.

Current architecture:

Weather cache:
15-minute TTL
500-entry bounded

Location cache:
24-hour TTL
500-entry bounded

Do NOT introduce Redis.

Do NOT introduce a database.

Do NOT overengineer for horizontal scaling yet.

Verify:

- expired entries are removed
- maximum entries are bounded
- different locations cannot contaminate each other
- stale weather fallback uses the correct cache entry
- alert cache is separate from weather cache

==================================================
PART K — PROVIDER FAILURE BEHAVIOR
==================================================

Verify all combinations:

Weather provider success
AQ provider success
AQ provider failure
Marine provider success
Marine provider failure
Alert provider success
Alert provider failure
Location provider failure

Desired behavior:

Core weather failure:
→ weather request fails appropriately

AQ failure:
→ weather still works
→ AQ fields null/unavailable

Marine failure:
→ weather still works
→ marine fields null/unavailable

Alert failure:
→ weather still works
→ alerts treated as unavailable

Location failure:
→ existing safe fallback behavior

Never return fabricated data.

==================================================
PART L — SOURCE TRANSPARENCY
==================================================

The UI must not misrepresent data provenance.

Where useful, show:

Weather:
"Source: Open-Meteo"

AQI:
"US EPA AQI"

Official warning:
"Source: IMD"

Marine:
"Marine forecast: Open-Meteo"

Do not clutter the UI.

Do not add large source banners.

A small source label or information affordance is sufficient.

==================================================
PART M — DATA FRESHNESS
==================================================

Do NOT claim that 15 minutes is a scientifically required weather refresh interval.

Treat:

15-minute cache

as an engineering freshness policy.

Ensure the UI can distinguish:

- current provider timestamp
- cache timestamp
- stale data

Do not display "Updated just now" unless actually justified.

==================================================
PART N — API SAFETY
==================================================

Verify:

- no provider API keys are committed
- no secrets are in React source
- no provider URLs are called directly from React
- request timeouts exist
- malformed provider responses do not crash the API
- bounded cache exists
- no infinite retry loops
- no unbounded background tasks

Do not add authentication.

Do not add a database.

==================================================
PART O — BACKEND RESPONSE CONTRACT
==================================================

Do not break:

WeatherResponse
LocationResult
autocomplete response

unless a backward-compatible extension is necessary.

If schema changes are required:

- make optional fields nullable where appropriate
- preserve existing fields
- update Pydantic validation
- test old responses/clients

==================================================
PART P — FRONTEND INTEGRATION
==================================================

Integrate the new optional data without redesigning the entire UI.

Existing dashboard must continue to work.

Handle:

AQI available
AQI unavailable

Marine available
Marine unavailable

Alerts available
No alerts
Alerts unavailable

Fresh weather
Stale weather
Weather unavailable

Do not display empty cards such as:

"Marine: null"

Use human-readable states.

==================================================
PART Q — PERSONALIZATION
==================================================

Do not rewrite personalizationEngine.js.

Ensure all existing interests still work:

Health
Fitness
Travel
Family
Agriculture
Commuting
Events
Beach & Surf

Beach & Surf should use marine data only when available.

If marine data is unavailable/inland:

the card should gracefully explain that marine conditions are unavailable/not applicable.

Do not invent surf recommendations.

==================================================
PART R — FINAL ERROR STATES
==================================================

Audit the dashboard for these states:

1. Weather loading
2. Weather success
3. Weather stale
4. Weather failure
5. AQI unavailable
6. Marine unavailable
7. No alerts
8. Alerts unavailable
9. Location search failure
10. Invalid location

All must have clean user-facing states.

No raw JSON.

No stack traces.

No "undefined".

No "NaN".

No "null".

No broken icons.

==================================================
PART S — TESTING
==================================================

Run backend tests and frontend build.

At minimum test:

Locations:
- Jaipur
- Mumbai
- Bengaluru
- Delhi
- Chennai
- London

Autocomplete:
- J
- Jai
- Jaipur
- Mum
- Mumbai
- Lon
- London
- invalid query

Weather:
- successful response
- cache hit
- cache expiry
- provider failure
- stale fallback
- stale cache expiration

AQI:
- available
- unavailable/null

Marine:
- inland location
- coastal location
- marine provider failure

Alerts:
- location with no alert
- location with an active official warning if available
- alert provider failure

Timezone:
- Jaipur
- London
- city switching

Personalization:
- all 8 interests
- multiple-interest combinations

==================================================
PART T — IMPORTANT LIVE-DATA RULE
==================================================

When testing official IMD alerts:

DO NOT manufacture a warning just to make the UI look populated.

If there is currently no warning for the tested location:

alerts = []

is correct.

If an official provider cannot be accessed without credentials:

document that fact.

Do not use a fake "IMD warning" and label it as live.

A demo/mock alert may only exist if it is explicitly marked as DEMO/MOCK and is kept separate from production/live data.

==================================================
PART U — UI CHANGES IN THIS STEP
==================================================

Keep UI changes minimal.

Only add what is necessary to correctly represent:

- alert state
- stale weather state
- marine availability
- source/semantics
- AQI standard

DO NOT begin the full UI/UX redesign yet.

That will be a separate phase after this task is stable.

==================================================
PART V — DOCUMENTATION
==================================================

Update project documentation if an existing architecture/progress document exists.

Document:

- weather provider
- AQI standard
- alert provider
- marine provider
- cache policy
- stale policy
- provider failure behavior
- known limitations
- official source access limitations

Do not create unnecessary documentation files.

==================================================
PART W — SECURITY / DEPLOYMENT READINESS AUDIT
==================================================

Without actually deploying yet, audit:

- environment variable usage
- CORS
- production API URL strategy
- debug/reload assumptions
- hardcoded localhost references
- provider secrets
- logging of sensitive data
- error responses
- dependency versions

Do not perform deployment in this task.

Do not install Docker.

Do not configure a production server.

Only report deployment blockers.

==================================================
PART X — FINAL REGRESSION
==================================================

After all implementation:

Run:

npm run build

Run backend tests.

Verify:

/api/health
/api/weather
/api/location/search

Verify browser console.

Verify no new errors/warnings.

Verify no mock weather data is used by the live dashboard.

Verify no provider API is called directly by the frontend.

==================================================
PART Y — FINAL REPORT — MANDATORY
==================================================

At the end provide a detailed report with:

1. Files created
2. Files modified
3. Files deleted
4. AQI decision and implementation
5. IMD source researched
6. IMD source actually integrated
7. Whether IMD authentication was required
8. Alert schema mapping
9. Location → district mapping strategy
10. Alert cache strategy
11. Marine provider
12. Marine fields implemented
13. Coastal detection strategy
14. Tide/sea-level semantics
15. Stale weather strategy
16. Maximum stale age
17. Cache behavior
18. Provider failure behavior
19. Source labeling
20. Personalization behavior
21. Frontend states added
22. Backend tests
23. Frontend tests
24. Live API tests
25. Build result
26. Browser console result
27. Security audit
28. Deployment blockers
29. Known limitations
30. Features deliberately deferred

For every feature clearly state:

IMPLEMENTED
DEFERRED
NOT POSSIBLE WITHOUT CREDENTIALS
NOT VERIFIED

Do not hide limitations.

==================================================
CRITICAL STOP CONDITION
==================================================

Do NOT start the final UI/UX redesign after this task.

Do NOT deploy after this task.

Do NOT add authentication/database.

Do NOT add push notifications.

Do NOT implement CPCB AQI from incomplete/instantaneous data.

Do NOT fabricate IMD alerts.

Do NOT fabricate marine/tide information.

STOP after the final report.