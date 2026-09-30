STEP 28 — FIX REMAINING DATA-QUALITY ISSUES BEFORE UI/UX POLISH

OBJECTIVE

Step 27 implemented most of the backend requirements, but the final audit identified four remaining issues:

1. IMD/Sachet alert location matching is not reliable enough.
2. There is no strong end-to-end proof that an active official alert is correctly returned for a matching location.
3. Autocomplete ranking is incorrect:
   "Mum" currently ranks Muli, Maldives above Mumbai.
4. 1-character autocomplete such as "J" still returns zero results.
5. The 15-minute fresh-cache vs 60-minute stale-cache behavior needs code-level verification.

This task must fix or verify ONLY these remaining issues.

DO NOT redesign the UI.
DO NOT add authentication.
DO NOT add a database.
DO NOT deploy.
DO NOT add push notifications.
DO NOT implement CPCB/NAQI AQI.
DO NOT implement astronomical tide tables.
DO NOT fabricate alerts, weather, marine data, or location results.

The existing verified functionality must remain intact.

--------------------------------------------------
PART 1 — INSPECT BEFORE MODIFYING
--------------------------------------------------

First inspect the current implementation of:

backend/services/weather_service.py
backend/services/alerts_service.py
backend/services/providers/imd_alerts.py
backend/services/location_service.py
backend/services/providers/open_meteo.py
backend/services/providers/base.py
backend/schemas/location.py
backend/schemas/weather.py
src/services/locationClient.js
src/components/onboarding/LocationAutocomplete.jsx

Also inspect all Step 27 tests.

Do not modify anything until you understand:

- weather cache lifecycle
- stale weather lifecycle
- alert lookup flow
- alert cache lifecycle
- location search flow
- autocomplete ranking
- LocationResult structure
- current IMD/Sachet matching logic

Preserve all previously approved behavior.

--------------------------------------------------
PART 2 — FIX AUTOCOMPLETE RANKING
--------------------------------------------------

Current regression:

Mum
→ Muli, Meemu Atholhu, Maldives
→ Mumbai, Maharashtra, India

This is incorrect.

Implement deterministic relevance ranking after provider results are received and before returning them.

Ranking priority:

1. Exact city-name match
2. City starts with query
3. City contains query
4. State/admin region starts with query
5. State/admin region contains query
6. Country relevance
7. Original provider order

Use only real provider data.

Normalize query and comparison strings using lowercase + trim.

Examples:

query = "Mumbai"

Mumbai should rank first.

query = "Mum"

Mumbai must rank before Muli.

Do not fabricate or manually insert unrelated locations.

Keep deduplication.

Keep maximum results at 10.

--------------------------------------------------
PART 3 — FIX 1-CHARACTER AUTOCOMPLETE
--------------------------------------------------

Current result:

J → []

This does not satisfy the intended UX.

First determine whether the current upstream provider genuinely supports reliable 1-character search.

Do not fabricate results.

If the provider does not reliably support 1-character queries, implement a bounded, verified local prefix fallback for 1-character searches.

Requirements:

- real city names only
- no invented locations
- useful Indian cities should be represented
- existing demo locations should be represented
- canonical data must include:
  city
  state
  country
  latitude
  longitude
  timezone
  displayName
- fallback dataset must remain bounded and maintainable
- clearly document that it is a local prefix fallback
- never silently map arbitrary queries to unrelated cities

For example:

J
→ Jaipur
→ Jodhpur
→ Jammu
→ Jalandhar

Only use locations backed by verified real location records.

For queries with 2+ characters, continue using the live provider.

If a safe 1-character implementation cannot be achieved without an unreasonable static dataset, document the limitation rather than fabricating data.

Do NOT regress:

Jai → Jaipur
Mum → Mumbai
Lon → London

--------------------------------------------------
PART 4 — PRESERVE CANONICAL LOCATION DATA
--------------------------------------------------

Every selected autocomplete result must continue to provide:

city
state
country
latitude
longitude
timezone
displayName

Weather must continue using the selected canonical location.

Verify:

Jaipur → Mumbai → Bengaluru → London

works correctly.

Verify interests remain unchanged when location changes.

--------------------------------------------------
PART 5 — IMPROVE IMD/SACHET ALERT LOCATION MATCHING
--------------------------------------------------

Current implementation primarily matches:

location.city

against:

CAP area_description

This is too weak.

Do NOT assume:

city == district

Inspect the actual Sachet/CAP payload and determine what geographic information is available.

Use the strongest reliable geographic matching strategy available.

Preferred matching order:

1. Exact district/administrative-area match if available.
2. Exact city/area match.
3. State + city/area match.
4. Coordinate/geographic matching only if reliable geographic metadata exists.
5. Otherwise return no alert instead of guessing.

Do NOT use crude substring matching where it can create false positives.

The matching logic must be deterministic and explainable.

Document exactly how a selected location is mapped to an alert.

--------------------------------------------------
PART 6 — DISTINGUISH NO ALERTS FROM ALERT SERVICE FAILURE
--------------------------------------------------

Maintain these semantics.

Successful provider check with no matching alert:

alerts = []
alertsAvailable = true

Meaning:

"No active matching official alerts were found."

Provider unavailable/failure:

alerts = []
alertsAvailable = false

Meaning:

"Official warning data could not currently be checked."

Never convert provider failure into "No alerts".

--------------------------------------------------
PART 7 — PROVE ACTIVE ALERT RETRIEVAL
--------------------------------------------------

Step 27 reported that Sachet contained live alerts, but the city regression showed zero alerts for all tested cities.

This is insufficient.

Inspect the actual live Sachet/CAP response.

Find at least one real active alert whose geographic area can be reliably associated with a supported test location.

Then prove this complete flow:

selected location
→ location/area matching
→ matching official CAP alert
→ WeatherAlertSchema
→ frontend-safe alert object

Verify:

- alert ID
- severity
- color
- title
- source
- warning message
- effective time
- expiry/end time where available

Do NOT create a fake production alert.

If no live alert can safely be reproduced at test time:

- create a test fixture from a captured REAL CAP response
- clearly mark it as a TEST FIXTURE
- do not use it in production
- separately document that live active-alert verification could not be reproduced

--------------------------------------------------
PART 8 — VERIFY ALERT TIME SEMANTICS
--------------------------------------------------

Review:

- issue time
- effective time
- expiry/end time

Do not label an expiry timestamp as the issue time.

If the existing WeatherAlertSchema only has one time field, preserve backward compatibility and document exactly which timestamp it represents.

If optional fields are necessary, they must be backward compatible.

Never invent timestamps.

--------------------------------------------------
PART 9 — VERIFY ALERT CACHE
--------------------------------------------------

Keep:

Alert cache TTL = 5 minutes.

Keep:

No stale emergency alerts.

Test:

Provider success
→ cache alert result
→ subsequent request can use cache.

Then simulate provider failure after cached data exists.

Expired alerts must NOT be returned as current alerts.

Expected:

alerts = []
alertsAvailable = false

Do not serve expired official alerts.

--------------------------------------------------
PART 10 — VERIFY WEATHER FRESH VS STALE CACHE
--------------------------------------------------

The intended behavior is:

0–15 minutes
→ fresh cached weather

15–60 minutes
→ stale fallback

isStale = true
dataAgeSeconds populated

More than 60 minutes
→ do not serve stale data
→ return provider error

IMPORTANT:

Do not accidentally delete the cached weather at 15 minutes if the stale fallback requires access to it.

The implementation must distinguish:

fresh-cache TTL = 15 minutes

from:

maximum stale retention = 60 minutes

Test all three states.

When stale weather is returned:

alerts = []
alertsAvailable = false

Never serve stale official alerts.

--------------------------------------------------
PART 11 — PREVENT CROSS-LOCATION CACHE CONTAMINATION
--------------------------------------------------

Test:

Jaipur
Mumbai
London

in sequence.

Verify:

Jaipur weather != Mumbai weather
Mumbai weather != London weather

Verify every weather cache key contains enough location information to prevent accidental reuse.

Never use a generic key such as:

"weather"

--------------------------------------------------
PART 12 — FRONTEND AUTOCOMPLETE REGRESSION
--------------------------------------------------

Do NOT redesign the autocomplete UI.

Verify:

J
Ja
Jai
M
Mum
Mumbai
Lon
London

Verify:

- loading state
- result ranking
- city/state/country display
- keyboard navigation
- Escape
- outside click
- selection
- canonical location persistence
- empty state
- provider failure
- no raw JSON
- no undefined/null rendering problems

Most importantly:

"Mum"

must show:

Mumbai, Maharashtra, India

before unrelated international results.

--------------------------------------------------
PART 13 — WEATHER REGRESSION
--------------------------------------------------

Verify all existing supported locations:

Jaipur
Mumbai
Bengaluru
Delhi
Chennai
London

For each verify:

- current weather
- hourly forecast
- daily forecast
- AQI
- UV
- sunrise/sunset
- personalization
- marine behavior
- alerts behavior
- timezone-aware greeting
- timezone-aware hourly "Now"

Do not modify the approved timezone/greeting logic unless a regression is discovered.

--------------------------------------------------
PART 14 — TEST ALL 8 PERSONALIZATION INTERESTS
--------------------------------------------------

Test:

Health
Fitness
Travel
Family
Agriculture
Commuting
Events
Beach & Surf

Verify:

- no null/undefined errors
- unavailable marine data handled safely
- unavailable AQI handled safely
- unavailable alerts handled safely
- stale weather handled safely
- interests remain unchanged after city switching

Do not unnecessarily rewrite personalizationEngine.js.

--------------------------------------------------
PART 15 — BUILD AND REGRESSION
--------------------------------------------------

Run:

npm run build

Run all backend tests.

Verify:

/api/health
/api/location/search
/api/weather

Check:

- HTTP status codes
- response schema
- malformed provider responses
- no raw exceptions
- no fabricated data
- no console errors
- no console warnings

--------------------------------------------------
PART 16 — FINAL REPORT
--------------------------------------------------

At the end provide a detailed report containing:

1. Files created
2. Files modified
3. Files deleted
4. Autocomplete ranking changes
5. 1-character autocomplete implementation
6. Example J results
7. Example Mum results
8. Alert matching strategy
9. How city/district ambiguity is handled
10. Active alert verification result
11. Whether active alert verification was LIVE or TEST FIXTURE
12. Alert schema mapping
13. Alert unavailable behavior
14. Alert cache behavior
15. Fresh weather cache behavior
16. Stale weather cache behavior
17. Exact stale-age boundaries tested
18. Cross-location cache test
19. Marine regression
20. AQI regression
21. All 8 personalization interests tested
22. City-switch regression
23. Timezone regression
24. Security regression
25. Backend test results
26. Frontend build result
27. Browser console result
28. Remaining limitations
29. Deliberately deferred features
30. Final verdict: whether backend/data layer is ready for UI/UX redesign

For every requirement classify it as:

IMPLEMENTED
VERIFIED
DEFERRED
NOT POSSIBLE WITHOUT EXTERNAL ACCESS
REMAINING LIMITATION

Do not hide unresolved issues.

--------------------------------------------------
IMPORTANT STOP CONDITION
--------------------------------------------------

After completing this task and reporting the results:

STOP.

Do NOT:

- redesign UI
- redesign dashboard
- add authentication
- add database
- deploy
- add push notifications
- implement CPCB AQI
- fabricate alerts
- fabricate tide data
- add unrelated features

The next task will be the dedicated UI/UX polish phase only after this report is reviewed and approved.