STEP 26 — COMPLETE TIMEZONE, GREETING & HOURLY FORECAST TIME CORRECTION

Goal:
Fix ALL time-related inconsistencies in the Mausam dashboard before moving to the remaining product requirements.

IMPORTANT:
This is a focused time/date correctness task.

Inspect the existing implementation first.

Do not modify:
- AQI
- IMD alerts
- marine
- tides
- authentication
- database
- deployment
- personalization logic unless required only for time correctness
- weather provider architecture

Do not add new dependencies unless absolutely necessary.

Do not change the overall visual design.

==================================================
1. BUG TO FIX — GREETING
==================================================

Current observed behavior:

At approximately 2:40 AM local time, the dashboard displays:

"Good morning, Kartik 👋"

This is incorrect for the desired product behavior.

Implement time-aware greeting logic using the SELECTED LOCATION'S LOCAL TIMEZONE.

Use these exact ranges:

00:00–04:59  → "Good night"
05:00–11:59  → "Good morning"
12:00–16:59  → "Good afternoon"
17:00–20:59  → "Good evening"
21:00–23:59  → "Good night"

Examples:

02:40 → Good night
04:59 → Good night
05:00 → Good morning
11:59 → Good morning
12:00 → Good afternoon
16:59 → Good afternoon
17:00 → Good evening
20:59 → Good evening
21:00 → Good night

Do not use the browser's current hour blindly.

==================================================
2. CRITICAL TIMEZONE REQUIREMENT
==================================================

The selected canonical location already contains:

canonicalLocation.timezone

Examples:

Jaipur:
Asia/Kolkata

London:
Europe/London

The dashboard's time-sensitive UI must use this timezone.

This includes at minimum:

- greeting
- current local time calculations
- hourly forecast labels
- "Now" determination
- displayed weather update time where applicable
- any Today/Tomorrow/day calculations that depend on current local time

Do NOT assume:

- Asia/Kolkata
- browser timezone
- system timezone
- UTC

The selected city's timezone is authoritative for the UI.

==================================================
3. HOURLY FORECAST BUG
==================================================

Current observed screenshot at approximately 02:40 AM:

Hourly forecast:

Now
1 AM
2 AM
3 AM
4 AM
5 AM
6 AM
...

This is incorrect.

The first hourly forecast item must correspond to the CURRENT/NEAREST CURRENT LOCAL FORECAST HOUR.

At approximately 02:40, the sequence should be based around the 02:00/03:00 local forecast boundary according to the actual provider timestamps.

Do NOT simply remove the first array element.

Do NOT hardcode "2 AM".

Do NOT assume the first item returned by the backend is always the current hour.

Instead inspect the actual backend hourly timestamps and determine the correct current/next forecast position.

==================================================
4. DETERMINE "NOW" CORRECTLY
==================================================

Inspect how the backend returns hourly timestamps.

Inspect how the frontend currently converts/parses them.

Do not use:

new Date("YYYY-MM-DDTHH:mm")

blindly if that causes JavaScript to interpret a provider-local timestamp using the browser timezone.

This is especially important when:

canonicalLocation.timezone !== browser timezone

Example:

User's browser:
Asia/Kolkata

Selected location:
Europe/London

London hourly timestamps must remain London local time.

Use a timezone-safe approach.

Prefer native Intl APIs / Intl.DateTimeFormat with IANA timezone support if no dependency is required.

Do not add moment.js/dayjs/luxon unless absolutely necessary.

==================================================
5. PRESERVE PROVIDER TIME SEMANTICS
==================================================

Do not modify backend weather timestamps unless the backend is demonstrably returning incorrect timestamps.

Open-Meteo provides timezone-aware/local forecast data.

First inspect the actual response.

Determine:

- hourly.time values
- current.time
- timezone
- generatedAt
- lastUpdated

Then fix the frontend interpretation.

Do not "fix" timestamps by adding/subtracting arbitrary hours.

No hardcoded +5:30.
No hardcoded -5:30.
No browser-offset arithmetic.

==================================================
6. HOURLY DISPLAY REQUIREMENT
==================================================

The hourly forecast should represent the next 10 relevant hourly forecast points.

The first item should be labeled:

"Now"

ONLY when it represents the current/nearest current forecast hour according to the selected location's local time.

Subsequent items should use:

1 AM
2 AM
3 AM
...

or:

12 AM
1 AM
...

as appropriate.

Do not show a past hour as the "Now" card.

For example, if local time is:

02:40

and hourly provider data is:

01:00
02:00
03:00
04:00
05:00
...

the display should NOT begin:

Now (01:00)

Instead it should use the current/nearest appropriate forecast point, based on the existing product convention.

If the current weather point is 02:00, it should be:

Now
3 AM
4 AM
5 AM
...

If the provider's first future/current point is 03:00, it should be:

Now
4 AM
5 AM
...

Use the actual data rather than hardcoding.

==================================================
7. CURRENT WEATHER VS HOURLY FORECAST
==================================================

Do not confuse:

current.time

with:

hourly.time[0]

They may not always be identical.

Use the current weather timestamp and hourly timestamps to determine which hourly point represents the current/nearest forecast period.

Inspect the actual implementation and choose a deterministic rule.

Document that rule in the final report.

==================================================
8. "UPDATED" TIMESTAMP
==================================================

The screenshot shows:

"Updated 02:30"

while the current time is around 02:40.

This may be valid if the provider's latest current-data timestamp is 02:30.

Verify this.

The application must NOT fabricate:

"Updated just now"

or generate a fake timestamp.

If lastUpdated comes from the provider, display it in the selected location's local timezone.

Example:

provider:
2026-09-30T02:30

timezone:
Asia/Kolkata

display:
Updated 02:30

If the provider timestamp is UTC, convert it correctly using the selected location timezone.

Do not apply arbitrary offsets.

==================================================
9. LONDON TEST — VERY IMPORTANT
==================================================

Because canonical location now contains timezone information, explicitly test:

Jaipur:
Asia/Kolkata

London:
Europe/London

Switch:

Jaipur → London

Verify:

1. Greeting uses London local time.
2. Hourly labels use London local time.
3. "Now" corresponds to London's current forecast period.
4. Weather update timestamp uses London's local timezone where applicable.
5. No India +5:30 offset is accidentally applied.
6. No browser timezone leakage occurs.

Then test:

London → Jaipur

and verify everything changes back correctly.

==================================================
10. DAY BOUNDARY TEST
==================================================

Test around midnight.

Verify:

23:xx
→ Good night

00:xx
→ Good night

04:59
→ Good night

05:00
→ Good morning

Also verify that hourly/day labels do not incorrectly remain on the previous calendar day.

==================================================
11. DST / INTERNATIONAL TIMEZONE SAFETY
==================================================

Do not manually calculate timezone offsets.

Use IANA timezone names from canonicalLocation.timezone.

This is important because locations such as London can change UTC offset seasonally.

The implementation must use the timezone database through supported JavaScript/Intl mechanisms rather than hardcoded offsets.

==================================================
12. NO VISUAL REDESIGN
==================================================

Keep the current UI exactly as it is visually wherever possible.

Only change:

- greeting text
- time labels
- hourly ordering
- update timestamp formatting if required

Do not redesign cards.

Do not change colors.

Do not change typography.

Do not change layout.

==================================================
13. REGRESSION TESTING
==================================================

Run:

- npm run build
- backend health
- backend weather endpoint
- existing location autocomplete
- existing personalization
- existing city switching

Verify:

Jaipur
Mumbai
Bengaluru
Delhi
London

No city should break.

==================================================
14. REQUIRED TIME TEST MATRIX
==================================================

Test greeting boundaries:

00:00 → Good night
02:40 → Good night
04:59 → Good night
05:00 → Good morning
11:59 → Good morning
12:00 → Good afternoon
16:59 → Good afternoon
17:00 → Good evening
20:59 → Good evening
21:00 → Good night
23:59 → Good night

Use controlled/mock time only for testing.
Do not modify production behavior to use mock time.

==================================================
15. REQUIRED HOURLY TEST
==================================================

At approximately local 02:40:

Verify that the displayed hourly sequence does NOT begin with:

Now
1 AM
2 AM
3 AM

unless the actual provider timestamps genuinely justify that.

The expected result should be aligned with the current/nearest local forecast hour.

Also test:

- morning
- afternoon
- evening
- midnight boundary

==================================================
16. IMPORTANT — FIND ROOT CAUSE, DON'T PATCH SYMPTOMS
==================================================

Do not simply:

- subtract one hour
- add one hour
- remove array[0]
- hardcode the current hour
- use browser local time
- add +5:30
- special-case Jaipur

Find the actual source of the mismatch.

Inspect:

- backend hourly timestamp generation
- weatherClient transformation
- Dashboard state
- HourlyForecast component
- date/time parsing
- timezone handling

Then fix the correct layer.

==================================================
17. FINAL REPORT — MANDATORY
==================================================

After implementation report:

1. Root cause of greeting bug
2. Root cause of hourly forecast bug
3. Files modified
4. Files created
5. Files deleted
6. Exact timezone handling approach
7. Exact greeting ranges
8. Exact "Now" determination rule
9. How provider timestamps are interpreted
10. How "Updated HH:MM" is generated
11. Jaipur test result
12. London test result
13. City-switch test result
14. Midnight-boundary test result
15. Greeting boundary test results
16. Hourly forecast test results
17. npm build result
18. Backend regression result
19. Console errors/warnings
20. Any unresolved limitations

IMPORTANT:

Do not start AQI work.
Do not start IMD alert work.
Do not start marine work.
Do not start stale-cache work.
Do not start deployment work.

This task is ONLY about fixing and verifying time/date/timezone behavior.

STOP after the report.