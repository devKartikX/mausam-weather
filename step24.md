STEP 25 — COMPLETE FRONTEND LOCATION AUTOCOMPLETE + CANONICAL LOCATION INTEGRATION

Goal:
Connect the existing React frontend to the new multi-result backend location-search API and implement a complete, polished, reliable location autocomplete flow.

This is a single consolidated implementation task.

IMPORTANT:
You are now allowed to modify the frontend and the location-search integration.

DO NOT:
- modify the weather provider
- modify WeatherService
- modify WeatherResponse
- modify AQI logic
- implement CPCB AQI
- implement IMD alerts
- implement marine weather
- implement tides
- implement stale-weather fallback
- add authentication
- add a database
- modify deployment infrastructure
- change personalizationEngine.js unless absolutely required for canonical location compatibility
- remove existing weather functionality
- replace real backend weather with mock data
- install unnecessary dependencies

The existing backend location endpoint is now:

GET /api/location/search?query=<query>

and returns:

List[LocationResult]

where each result contains:

{
  city,
  state,
  country,
  latitude,
  longitude,
  timezone,
  displayName
}

The existing weather endpoint remains intact.

==================================================
PART 1 — AUDIT THE EXISTING FRONTEND FIRST
==================================================

Before modifying anything, inspect:

- PersonalizationScreen / onboarding flow
- current location input
- userProfile state shape
- localStorage persistence
- Dashboard
- weatherClient.js
- any existing location-related components/styles
- personalizationEngine.js
- existing navigation between onboarding and dashboard

Understand how the current free-text city/location value flows into the weather request.

Do not blindly replace the existing flow.

Preserve existing onboarding behavior for:
- name
- interests
- personalization
- localStorage
- navigation

==================================================
PART 2 — CREATE FRONTEND LOCATION SEARCH CLIENT
==================================================

Create or extend a small frontend service responsible for location search.

Use:

GET /api/location/search?query=<encoded query>

Do NOT call Open-Meteo directly from React.

The frontend must only communicate with our FastAPI backend.

Handle:
- HTTP errors
- empty results
- network failures
- request cancellation/race conditions

Do not expose provider URLs or provider-specific logic in React.

==================================================
PART 3 — DEBOUNCED AUTOCOMPLETE
==================================================

Implement a debounced autocomplete.

Target debounce:
approximately 300ms.

Behavior:

User types:

J
Ja
Jai
Jaip

The application must NOT send a network request for every keystroke immediately.

Use a debounce around 250–300ms.

IMPORTANT:
Do NOT hardcode a 2-character minimum.

The product requirement allows a one-character query such as:

J

However, the backend/provider may legitimately return [] for a one-character query.

The frontend must handle that gracefully.

Recommended behavior:

- query length 0:
  no request, close/clear suggestions

- query length >= 1:
  allow autocomplete request

- if provider returns []:
  show a subtle "No matching cities found" state rather than an error

Do not fabricate suggestions.

==================================================
PART 4 — AUTOCOMPLETE DROPDOWN UI
==================================================

Replace the current plain location input behavior with a proper autocomplete dropdown.

Each suggestion should clearly display:

CITY
STATE/REGION, COUNTRY

Example:

Jaipur
Rajasthan, India

Jodhpur
Rajasthan, India

London
England, United Kingdom

Prefer displayName where appropriate, but make the visual hierarchy clear.

Requirements:

- dropdown appears below the location input
- suggestions are easy to tap on mobile
- minimum comfortable touch target around 44px
- keyboard-friendly on desktop
- clear selected/hovered state
- dropdown should not overflow the viewport
- maintain the existing visual design language
- do not introduce a completely different UI style
- support 320px mobile width
- support tablet and desktop

Do not add unnecessary animations.

==================================================
PART 5 — LOADING / EMPTY / ERROR STATES
==================================================

Autocomplete must have clear states.

While searching:

"Searching locations..."

No results:

"No matching cities found"

Network/backend failure:

"Couldn't search locations. Try again."

These states should be visually subtle and should not look like a catastrophic application error.

Do not display raw FastAPI errors to the user.

==================================================
PART 6 — RANKING / RESULT QUALITY
==================================================

The backend currently returns up to 8 results.

Do not invent locations.

Preserve the backend results.

However, inspect the returned results and ensure the frontend does not unnecessarily reorder them in a way that destroys provider relevance.

For Indian results, the displayed state and country must remain visible so ambiguous names can be distinguished.

Example:

Bilaspur
Chhattisgarh, India

Bilaspur
Himachal Pradesh, India

Do NOT display only:

Bilaspur

because this creates ambiguity.

==================================================
PART 7 — SELECTION MUST STORE CANONICAL LOCATION
==================================================

This is one of the most important requirements.

When the user selects a suggestion, DO NOT store only:

location: "Jaipur"

Instead store the canonical selected location information:

{
  city: "Jaipur",
  state: "Rajasthan",
  country: "India",
  latitude: 26.xxxxx,
  longitude: 75.xxxxx,
  timezone: "Asia/Kolkata",
  displayName: "Jaipur, Rajasthan, India"
}

Adapt the exact userProfile structure to the existing application architecture rather than unnecessarily redesigning the whole state model.

The important requirement is that the selected location retains:

- city
- state
- country
- latitude
- longitude
- timezone
- displayName

==================================================
PART 8 — WEATHER REQUEST MUST USE CANONICAL LOCATION
==================================================

After selection, the dashboard/weather flow must remain correct.

IMPORTANT:

Do not blindly pass the displayed string back into geocoding every time.

The selected canonical location should be retained in frontend state/localStorage.

If the existing weather endpoint currently accepts the city query and internally resolves it, DO NOT break that contract during this step.

Instead:

1. preserve current working weather behavior
2. retain canonical coordinates for future direct-coordinate weather support
3. ensure the selected city is what the dashboard displays
4. ensure weather reloads correctly after changing the location

Do not modify the backend weather endpoint in this task.

==================================================
PART 9 — LOCALSTORAGE
==================================================

Update persistence so the selected canonical location survives page reload.

For example, the stored profile may contain:

location: {
  city,
  state,
  country,
  latitude,
  longitude,
  timezone,
  displayName
}

But adapt this to the existing userProfile structure if a compatible structure already exists.

Backward compatibility is required.

If an existing user has an older localStorage format containing only:

location: "Jaipur"

the application must NOT crash.

Gracefully support the old format.

If necessary, migrate it when a new canonical location is selected.

Do not delete existing user preferences.

==================================================
PART 10 — CITY CHANGE BEHAVIOR
==================================================

Test this exact flow:

Initial:
Jaipur

Then user changes to:

Mumbai

Then:

Bengaluru

Then:

London

For every selection:

- old weather must not remain visible after the new location is selected
- loading state should appear appropriately
- new weather must correspond to the selected city
- personalization interests must remain unchanged
- selected canonical location must persist
- no race condition should allow an older request to overwrite the newest selection

Also test:

Jaipur → London → Jaipur

to ensure the state remains correct.

==================================================
PART 11 — RACE CONDITION PROTECTION
==================================================

Autocomplete requests can overlap.

Example:

User types:

J
Ja
Jai
Jaip

A slower response for "Ja" must NOT overwrite a newer response for "Jaip".

Use the existing project's preferred approach, such as:

- AbortController
- request identity
- cancellation flag

Do not introduce a complex state-management library.

The latest query must win.

Similarly, selecting a location while an autocomplete request is still pending must close/ignore stale suggestions appropriately.

==================================================
PART 12 — DROPDOWN INTERACTION
==================================================

Support:

- click/tap suggestion
- keyboard navigation if practical
- Escape closes dropdown
- clicking outside closes dropdown
- selecting a result closes dropdown
- input reflects selected city/displayName
- focus behavior remains natural

Do not make the user manually type the full city after selecting a suggestion.

==================================================
PART 13 — ONE-CHARACTER QUERY REQUIREMENT
==================================================

This is important.

The backend test showed:

query="J"

may return:

[]

because of provider behavior.

DO NOT fabricate results.

If "J" returns no results:

- keep the UI functional
- show no-results state
- allow the user to continue typing
- "Ja" / "Jai" should trigger another search
- do not treat [] as a backend failure

If the existing offline fallback naturally provides results for one-character queries, display them normally.

Do not create a large hardcoded city database in this step just to force "J" to return results.

If the provider limitation makes one-character search fundamentally ineffective, document this clearly in the final report rather than creating fake data.

==================================================
PART 14 — ACCESSIBILITY
==================================================

Make the autocomplete reasonably accessible.

Use appropriate:

- aria-label
- aria-expanded
- aria-controls
- role="listbox"
- role="option"

where appropriate.

Ensure keyboard focus is visible.

Do not rely solely on color to communicate selection.

The autocomplete must remain usable on mobile.

==================================================
PART 15 — VISUAL INTEGRATION
==================================================

The autocomplete should look like part of the existing Mausam product.

Do not redesign the entire onboarding screen.

Only improve what is necessary for:

- location input
- dropdown
- loading state
- empty state
- error state
- selected location

Keep existing typography, spacing, cards, borders, radius, and overall visual language wherever possible.

This is functional integration, NOT the final UI/UX polish phase.

==================================================
PART 16 — BACKWARD COMPATIBILITY
==================================================

Existing users may have localStorage data from before canonical location support.

Test at least:

Case A:
No existing localStorage.

Case B:
Old profile with:

location: "Jaipur"

Case C:
New profile with canonical location object.

None should crash the application.

==================================================
PART 17 — REGRESSION TESTING
==================================================

Run and verify:

1. Frontend build
2. Backend health endpoint
3. Backend weather endpoint
4. Backend location search endpoint
5. Existing onboarding flow
6. Name persistence
7. Interest persistence
8. Personalization engine
9. Dashboard weather loading
10. Weather error/retry behavior
11. City switching
12. London timezone behavior
13. Mobile 320px layout
14. Tablet layout
15. Desktop layout
16. Browser console

Console should have no new errors or warnings.

==================================================
PART 18 — REQUIRED MANUAL TEST MATRIX
==================================================

Test these queries:

J
Ja
Jai
Jaipur
Mum
Mumbai
Del
Delhi
Ben
Bengaluru
Lon
London
xyzrandomcity123

Verify:

- reasonable suggestions where provider supports them
- city/state/country shown
- no fabricated locations
- no silent remapping
- empty results handled correctly
- selection works
- selected canonical data persists

==================================================
PART 19 — IMPORTANT ARCHITECTURAL RESTRICTIONS
==================================================

Do NOT:

- add CPCB AQI
- add IMD alerts
- add marine data
- add tides
- add authentication
- add database
- replace Open-Meteo
- modify weather schema
- modify backend weather service
- modify weather provider
- add a giant city dataset
- hardcode weather data
- reintroduce mockWeather
- bypass FastAPI and call Open-Meteo from frontend

The only backend interaction required is the existing location search API.

==================================================
PART 20 — FINAL REPORT — MANDATORY
==================================================

When implementation is complete, provide a detailed report containing:

1. Files created
2. Files modified
3. Files deleted
4. Existing files inspected
5. Exact userProfile/location state shape after implementation
6. Exact localStorage shape after implementation
7. Autocomplete request/debounce behavior
8. Empty/loading/error behavior
9. Race-condition protection
10. Keyboard/mobile behavior
11. Accessibility implementation
12. Backward compatibility behavior
13. City-switch behavior
14. Exact API integration
15. Manual test results for:
    - J
    - Ja
    - Jai
    - Jaipur
    - Mum
    - Mumbai
    - Del
    - Delhi
    - Ben
    - Bengaluru
    - Lon
    - London
    - xyzrandomcity123
16. Build result
17. Console result
18. Backend regression result
19. Any limitations, especially the one-character "J" provider limitation
20. Any assumptions

Clearly distinguish:
- implemented
- tested
- not implemented
- limitation

MANDATORY:
Do not start AQI, IMD alerts, marine, stale cache, authentication, or deployment work after completing this task.

STOP after the report.
