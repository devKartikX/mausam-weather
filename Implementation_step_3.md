IMPLEMENT STEP 3 — MOCK WEATHER DATA + DASHBOARD SHELL ONLY

Step 2 is complete. Now build the foundation of the actual Mausam weather dashboard.

IMPORTANT:
This step has TWO goals only:
1. Create realistic mock weather data.
2. Build the main dashboard shell that displays that data.

Do NOT implement interest-based personalization yet.
Do NOT create the personalization engine yet.
Do NOT create specialized Health/Fitness/Travel/etc. cards yet.
Do NOT add real weather APIs.
Do NOT add backend/database/authentication.
Do NOT add a persona switcher.
Do NOT redesign or rebuild the onboarding screen unless required for integration.

DATA:

Create:
src/data/mockWeather.js

Use realistic mock data for Jaipur, Rajasthan, India.

Include enough structured data for:

- location
- current temperature
- weather condition
- feels-like temperature
- humidity
- wind speed
- wind direction
- precipitation probability
- visibility
- UV index
- AQI
- sunrise
- sunset
- hourly forecast for approximately 8 hours
- 7-day forecast
- at least one weather alert

Keep the data as plain JavaScript objects/arrays.

Example structure:

weatherData = {
  location: {...},
  current: {...},
  hourly: [...],
  daily: [...],
  alerts: [...]
}

Do not fetch anything from the internet.

DASHBOARD:

Create the main dashboard UI inside:

src/components/dashboard/

Build these sections:

1. HEADER
- Mausam branding
- Current city/location
- Simple settings/profile icon if useful
- Clean mobile-friendly layout

2. PERSONALIZED GREETING AREA
For now use the profile data already captured by Step 2.

Example:
"Good evening, Kartik"
"Here's your weather outlook for Jaipur"

Do not yet change content based on interests.

3. CURRENT WEATHER HERO
Display prominently:
- current temperature
- weather condition
- feels like
- appropriate weather icon
- location

4. KEY WEATHER METRICS
Display a clean group of metrics:
- Humidity
- Wind
- Rain probability
- Visibility
- UV index
- AQI

5. HOURLY FORECAST
Create a horizontally scrollable mobile-friendly hourly forecast.

Each item should show:
- time
- weather icon
- temperature
- rain probability if appropriate

6. 7-DAY FORECAST
Create a clean vertical or compact forecast list.

Each day should show:
- day
- weather icon
- condition
- high temperature
- low temperature
- rain probability

7. WEATHER ALERT
Create a visually distinct alert section using the mock alert data.

8. BOTTOM / PROFILE ACTION
Provide a simple "Edit Preferences" action that returns to the Step 2 personalization screen.

INTEGRATION:

Connect the existing Step 2 state to the dashboard.

Flow should now become:

Personalization Screen
        ↓
User enters name + location + interests
        ↓
Create My Dashboard
        ↓
Dashboard
        ↓
Dashboard displays captured name/location

The selected interests should be preserved, but DO NOT use them to personalize content yet.

The temporary DashboardPlaceholder should no longer be the final destination after submission. Replace it with the new dashboard.

If the user clicks "Edit Preferences":
Dashboard
   ↓
Edit Preferences
   ↓
Personalization Screen
   ↓
previous name/location/interests remain populated

DESIGN:

Use the existing design system from Step 1.

Requirements:
- Premium modern weather-app appearance
- Mobile-first
- Responsive desktop layout
- Strong visual hierarchy
- Large current-temperature hero
- Clean cards
- Rounded corners
- Subtle shadows
- Consistent spacing
- Lucide icons
- Minimal animations
- Avoid excessive gradients
- Avoid excessive glassmorphism
- Avoid clutter

The dashboard should feel like a real weather application, not an admin dashboard.

COMPONENT STRUCTURE:

Create reusable dashboard components where useful, for example:

src/components/dashboard/
├── Dashboard.jsx
├── WeatherHero.jsx
├── WeatherMetrics.jsx
├── HourlyForecast.jsx
├── DailyForecast.jsx
└── WeatherAlert.jsx

Do not create unnecessary abstractions.

IMPORTANT:
Keep the mock data separate from UI components.
Do not hard-code weather values throughout JSX.

VERIFICATION:

1. Run npm run build.
2. Run the development server.
3. Test the complete flow:
   Personalization → Dashboard → Edit Preferences → Personalization.
4. Verify captured name and location appear correctly on the dashboard.
5. Verify hourly and daily forecast render correctly.
6. Verify alert renders correctly.
7. Verify responsive behavior.
8. Check browser console for errors.

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
- Report whether npm run build passed.
- Report whether the dev server was tested.
- Report whether the complete user flow was tested.
- Report whether browser/console testing was performed.
- Mention any errors or warnings.

6. DEVIATIONS / ISSUES
- Explicitly mention anything that could not be implemented exactly as requested.
- Mention any assumptions or decisions you made.

7. CURRENT PROJECT STATE
- Briefly describe what is now working.
- Clearly state what remains intentionally unimplemented.

STOP HERE.
Do not continue to personalization logic or additional features beyond this prompt.