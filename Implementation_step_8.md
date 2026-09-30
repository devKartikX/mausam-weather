FIX — Correctness and Demo Data Honesty

Make ONLY the targeted fixes below. Do not redesign the app, add new features, change the personalization architecture, or modify the existing 8-interest logic.

1. FIX DAILY FORECAST LOCATION
- In DailyForecast, remove the hardcoded "Jaipur District".
- Use the user's entered location from the existing app state/props.
- Display the entered city/location dynamically.
- Do not introduce a new location system.

2. FIX WEATHER HERO LOCATION
- WeatherHero currently derives/displays the state from mock data, which can produce incorrect output such as "Mumbai, Rajasthan".
- The user's entered location should be the primary displayed location.
- Do not claim a state/region unless it is actually known from the entered location.
- If the prototype only knows the typed city string, simply display that city/location.

3. FIX WEATHER METRIC SUB-LABELS
- Remove static labels such as:
  "Comfortable"
  "Low probability"
  "Good visibility"
- Make the secondary labels reflect the actual mock values.
- Keep the logic simple and deterministic.
- Examples:
  - Rain probability should describe the actual probability range.
  - Visibility should describe the actual visibility value.
  - Humidity should describe the actual humidity value.
- Do not introduce complex weather calculations.

4. MAKE MOCK DATA OBVIOUSLY DEMO DATA
- The prototype uses mock weather data and must NOT imply that the displayed weather is live official IMD data.
- Replace wording such as "Updated Just now" with something like:
  "Demo weather data"
  or another equally clear concise label.
- WeatherAlert/advisory content must clearly indicate that it is a DEMO/SIMULATED advisory.
- Keep the existing visual design; do not add a large warning banner.
- Do not claim real-time API/IMD data.

5. SOFTEN FAMILY + AGRICULTURE WORDING
- Keep the existing personalization logic.
- Do not remove the insights.
- Adjust wording that sounds overly certain or prescriptive.
- Family advice should use language such as "consider", "may help", or "it may be useful to".
- Agriculture advice should similarly avoid presenting weather-based guidance as guaranteed agricultural/chemical advice.
- Preserve the useful weather context and metrics.

IMPORTANT:
- Do not modify Health, Fitness, Travel, Commuting, Events, or Beach & Surf logic.
- Do not add APIs, backend services, authentication, database, ML, or new dependencies.
- Do not perform visual redesign in this step.
- Reuse the existing state/data flow wherever possible.
- Keep the implementation minimal and prototype-friendly.

After making the changes, run the existing build and test the affected UI paths.

REPORT BACK AFTER COMPLETION:

Before stopping, provide a concise implementation report containing:

1. WHAT YOU DID
- Describe exactly what was implemented/changed.

2. FILES CHANGED
- List every file created, modified, or deleted.
- For each file, briefly explain its purpose.

3. UI / BEHAVIOR CHANGES
- Describe what the user can now see and do.
- Mention important interactions and state changes.

4. TECHNICAL CHANGES
- Mention important components, state, functions, data structures, dependencies, or logic added.

5. VERIFICATION
- Report whether `npm run build` passed.
- Report whether the dev server was tested.
- Report whether browser/console testing was performed.
- Mention any errors or warnings found.

6. DEVIATIONS / ISSUES
- Explicitly mention anything that could not be implemented exactly as requested.
- Mention any assumptions or decisions you made.

7. CURRENT PROJECT STATE
- Briefly describe what is now working.
- Clearly state what remains intentionally unimplemented.

STOP HERE.
Do not continue to the next feature or make additional changes beyond this prompt.