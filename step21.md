STEP 21 — REAL-DATA FRONTEND AUDIT AND HARDENING

Goal:
Audit the entire existing React dashboard now that it consumes live backend weather data, identify any real-data issues, and fix only issues discovered during this audit.

IMPORTANT:
This is an implementation + verification task.
Do NOT add new major features.
Do NOT add authentication or database.
Do NOT deploy.
Do NOT redesign the application.
Do NOT change the personalization strategy.
Keep the existing UI/design language.

The objective is to make sure the existing polished frontend behaves correctly with real-world weather data rather than demo/mock assumptions.

==================================================
TASK 1 — AUDIT THE COMPLETE WEATHER DATA FLOW
==================================================

Trace the live data from:

userProfile.location
→ weatherClient
→ /api/weather
→ Dashboard state
→ existing dashboard components
→ personalizationEngine

Confirm every displayed weather value originates from the live backend response.

Search the frontend for:

- mockWeather
- mockWeatherData
- hardcoded Jaipur
- hardcoded Rajasthan
- hardcoded weather values
- hardcoded AQI
- hardcoded temperature
- hardcoded sunrise/sunset
- hardcoded hourly values
- hardcoded daily values
- demo-only weather assumptions

Do not delete mockWeather.js.

Remove/fix any remaining runtime demo dependency if found.

==================================================
TASK 2 — AUDIT THE DASHBOARD DATA CONTRACT
==================================================

Inspect every component that consumes weatherData.

Verify handling of:

current
location
hourly
daily
alerts
AQI
UV
wind
visibility
sunrise
sunset
marine fields

For every field, determine:

1. Is it always available?
2. Can it be null?
3. Can an API/provider failure make it unavailable?
4. Does the UI crash or display misleading information if unavailable?

Fix only genuine issues.

Do NOT add unnecessary defensive code everywhere.

==================================================
TASK 3 — NULL / UNAVAILABLE DATA
==================================================

The backend intentionally returns null for unavailable marine information:

waveHeight
seaSurfaceTemp
tidalInfo

and AQI can also be unavailable if the Air Quality API fails.

Verify the frontend handles these cases safely.

Rules:

- Never display "0" when the real value is unavailable.
- Never display fabricated weather information.
- Never display "0%" merely because rain probability is missing.
- Never display fake AQI.
- Never display fake marine/tide information.

Use the application's existing visual language for unavailable values, such as:

"Unavailable"
or
"Not available"

only where appropriate.

Do not redesign cards.

==================================================
TASK 4 — AQI LABELING
==================================================

Verify that the frontend does not imply that the AQI value is CPCB/Indian AQI.

The backend currently provides US EPA AQI semantics.

Where AQI is presented prominently, ensure the UI makes the semantics sufficiently clear.

Prefer a concise treatment consistent with the existing design.

Do not rewrite the AQI system.

==================================================
TASK 5 — WEATHER TIME / TIMESTAMP AUDIT
==================================================

Inspect all timestamps displayed by the dashboard.

Verify:

- location timezone is respected
- hourly labels correspond to the selected city's local timezone
- daily day names correspond to the selected city's local date
- sunrise/sunset are local
- no browser-local timezone accidentally overrides provider-local weather times

Pay particular attention to London vs Indian cities.

Do not introduce a second timezone conversion system if the backend already returns correctly formatted local values.

==================================================
TASK 6 — HOURLY FORECAST AUDIT
==================================================

Verify the hourly component with real backend data.

Check:

- exactly 10 records are handled
- first item is "Now"
- subsequent times display correctly
- temperatures match backend data
- precipitation probability matches backend data
- condition/icon mapping remains correct
- no undefined values appear

Also inspect whether the frontend assumes a fixed number of hourly items.

If the UI breaks when fewer records are received, make the smallest safe correction.

==================================================
TASK 7 — DAILY FORECAST AUDIT
==================================================

Verify:

- exactly 7 days are displayed
- first day is "Today"
- remaining days use the backend-provided local dates/day labels
- high/low temperatures are correct
- precipitation probability is correct
- condition/icon is correct

Check for array-index assumptions.

Do not change the 7-day product requirement.

==================================================
TASK 8 — CURRENT WEATHER METRICS
==================================================

Verify the following:

temperature
feelsLike
highTemp
lowTemp
humidity
windSpeed
windDirection
rainProbability
visibility
uvIndex
uvStatus
aqi
aqiStatus
pm25
pm10
sunrise
sunset

Make sure:

- no field is accidentally swapped
- no unit is wrong
- no stale mock value remains
- null values are safe
- numeric zero is not treated as missing

Pay particular attention to values where 0 is valid, such as:

UV = 0
rain probability = 0
wind speed = 0
AQI = 0

Do not use generic truthiness checks that incorrectly hide valid zero values.

==================================================
TASK 9 — PERSONALIZATION REGRESSION
==================================================

Do not modify:

src/services/personalizationEngine.js

Run the existing personalization logic against live weather for multiple profiles.

At minimum test:

1. Health + Fitness
2. Travel + Commuting
3. Agriculture
4. Beach & Surf
5. Family
6. Events

Verify:

- personalization does not crash
- cards render
- real weather values are used
- missing marine data does not cause Beach & Surf to fabricate information
- changing interests still changes the personalized content

Do not redesign or re-score the personalization engine.

==================================================
TASK 10 — CITY CHANGE / EDIT PREFERENCES
==================================================

Test the complete user flow:

Onboarding
→ choose city
→ dashboard
→ edit preferences
→ change city
→ dashboard reloads weather

Verify:

- old weather does not remain visible after the city changes
- new city triggers a new API request
- loading state appears
- new city weather appears
- personalization updates using the new weather
- existing interests remain intact

Test at least:

Jaipur → Mumbai
Mumbai → Bengaluru
Bengaluru → London

==================================================
TASK 11 — PAGE REFRESH / PERSISTENCE
==================================================

Refresh the browser while on the dashboard.

Verify:

- existing user profile persistence still works
- city is restored
- weather is fetched again
- no mock weather appears
- no crash occurs
- loading state behaves correctly

Do not introduce a new persistence mechanism.

==================================================
TASK 12 — ERROR / RETRY AUDIT
==================================================

Test:

1. Backend unavailable
2. Invalid/unresolvable city where reachable through the UI
3. Successful retry after a temporary failure

Verify:

- loading ends
- error state appears
- retry works
- successful retry replaces error state
- no mock weather is shown
- no stale weather is silently presented as current

Do not expose stack traces.

==================================================
TASK 13 — RESPONSIVE / REAL CONTENT AUDIT
==================================================

Test the dashboard with actual live data on:

- mobile-width viewport
- tablet-ish width
- desktop width

Look specifically for:

- overflow
- clipped text
- AQI text wrapping
- long city names
- long condition names such as "Moderate Rain Showers"
- hourly forecast overflow
- personalization card overflow
- error/loading state overflow

Use existing responsive patterns.

Make only targeted CSS fixes if a genuine problem is found.

Do not redesign the layout.

==================================================
TASK 14 — ACCESSIBILITY / UI REGRESSION
==================================================

Verify:

- retry button is keyboard accessible
- loading state is understandable
- error state is understandable
- interactive elements remain usable
- no console warnings are introduced
- existing icons have appropriate accessibility treatment where applicable

Do not perform a full accessibility redesign.

==================================================
TASK 15 — REAL DATA TEST MATRIX
==================================================

Run the application with:

Jaipur
Mumbai
Bengaluru
Delhi
Kolkata
Chennai
London

For each city verify at minimum:

- location
- current temperature
- condition
- humidity
- wind
- AQI if available
- hourly forecast
- daily forecast
- sunrise/sunset

Do not require exact weather values because provider data changes.

The goal is correct rendering and data flow.

==================================================
TASK 16 — CODE QUALITY CHECK
==================================================

Inspect the changes from Steps 19–21 for:

- duplicated weather transformations
- unnecessary state
- stale imports
- unused variables
- dead code
- incorrect React effect dependencies
- accidental repeated API requests
- request loops
- race conditions when changing cities

Pay particular attention to:

useEffect(...)
loadWeather(...)
weatherData
userProfile.location

If a user changes city rapidly, ensure an older response cannot incorrectly overwrite the newer city's weather.

Only fix a race condition if one actually exists or is clearly possible from the implementation.

==================================================
TASK 17 — BUILD + FINAL REGRESSION
==================================================

Run:

- frontend production build
- backend health check
- backend weather endpoint
- frontend integration
- console error/warning check

Confirm:

- build passes
- no runtime errors
- no console errors
- no console warnings caused by this step
- backend remains functional
- frontend remains functional

==================================================
IMPORTANT BOUNDARIES
==================================================

DO NOT:

- modify personalizationEngine.js
- add authentication
- add database
- add user accounts
- add deployment configuration
- integrate IMD
- integrate tides
- add official government alerts
- add another weather provider
- redesign Dashboard
- redesign onboarding
- redesign personalization cards
- delete mockWeather.js
- remove existing profile persistence
- change interest categories
- change personalization scoring
- replace Open-Meteo
- introduce a global state library
- introduce unnecessary dependencies

Only fix issues discovered by this audit.

If the audit finds no issue in a particular area, leave it unchanged.

==================================================
MANDATORY REPORTING
==================================================

After completion, report:

1. Exact files created
2. Exact files modified
3. Exact files deleted
4. Remaining runtime references to mockWeather
5. Data-contract issues found
6. Null/unavailable-data issues found
7. AQI labeling result
8. Timezone audit result
9. Hourly forecast audit result
10. Daily forecast audit result
11. Current metrics audit result
12. Personalization regression results for all tested profiles
13. City-change test results
14. Page-refresh/persistence result
15. Backend failure result
16. Retry result
17. Responsive/mobile result
18. Accessibility regression result
19. Race-condition/useEffect audit result
20. Cities tested
21. Console result
22. Production build result
23. Every code fix made and why
24. Any remaining concerns
25. Any assumptions
26. Any deviations

IMPORTANT:
If you discover a serious architectural problem that should NOT be fixed in this step, report it clearly instead of making a large change.

Then STOP.

Do not proceed to Step 22.