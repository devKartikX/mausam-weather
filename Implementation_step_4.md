IMPLEMENT STEP 4 — PERSONALIZATION ENGINE + FIRST PERSONALIZED INSIGHTS

Steps 1–3 are complete.

The project currently has:
- React/Vite foundation
- Personalization onboarding
- User name, location and selected interests stored in App state
- Mock Jaipur weather data
- Working weather dashboard
- Edit Preferences flow

Now implement the FIRST real personalization layer.

CORE GOAL:

The Mausam dashboard must now visibly change based on the user's selected interests.

For this step, build:
1. A simple deterministic personalization engine.
2. A reusable personalized insight card.
3. Personalized insights for ONLY:
   - Health
   - Fitness
   - Travel
   - Commuting

Do NOT implement the remaining interests yet:
- Family
- Agriculture
- Events
- Beach & Surf

Do NOT add:
- real weather APIs
- backend/database
- authentication
- ML/AI model
- complex recommendation algorithms
- persona switcher
- external services

PERSONALIZATION ENGINE:

Create:

src/services/personalizationEngine.js

Keep the logic simple and deterministic.

The engine should receive:
- selected interests
- current/mock weather data

It should return an array of personalized insight objects.

Conceptually:

selectedInterests + weatherData
            ↓
personalizationEngine
            ↓
personalizedInsights[]

Each insight should contain enough information for the UI, such as:
- interest/category
- title
- short explanation
- relevant metrics
- recommendation
- severity/status where useful
- Lucide icon identifier if needed

Do NOT hard-code complete UI markup inside the engine.

The engine should only decide WHAT personalized information should be shown.

PERSONALIZED INSIGHTS:

1. HEALTH

When Health is selected, show information based on:
- AQI
- UV index
- humidity
- temperature

Example concept:

Title:
"Health & Air Quality"

Information:
"AQI is 138 (Moderate). UV index is 6 (High)."

Recommendation:
"Limit prolonged outdoor exposure during peak afternoon hours."

Use the actual mock weather values instead of hard-coded values wherever possible.

2. FITNESS

When Fitness is selected, show:
- temperature
- feels-like temperature
- AQI
- UV
- rain probability
- wind

Create a simple activity assessment such as:
"Good for outdoor activity"
or
"Better to exercise later"

The assessment must be derived from the mock weather data using simple understandable conditions.

3. TRAVEL

When Travel is selected, show:
- rain probability
- current condition
- visibility
- temperature
- weather alert status

Example:
"Travel conditions are mostly favorable, but carry rain protection if precipitation probability increases."

Again, derive the information from the existing mock data.

4. COMMUTING

When Commuting is selected, show:
- rain probability
- visibility
- wind
- weather condition
- active alert if relevant

Provide a concise commute recommendation such as:
"Visibility is good, but keep an eye on the afternoon advisory."

Do not claim real-time road/traffic information.

REUSABLE COMPONENT:

Create:

src/components/personalized/PersonalizedInsightCard.jsx

The component should receive an insight object as props and render:
- category/icon
- title
- short explanation
- relevant weather metrics
- recommendation
- appropriate status styling

The card should work for all four categories without duplicating UI code.

DASHBOARD INTEGRATION:

Add a dedicated section to the dashboard:

"Personalized for you"

or similar wording.

Position it prominently:
- after the greeting/current-weather hero
- before the generic forecast sections

Example:

Good evening, Kartik 👋
Here's your weather outlook for Jaipur

[Current Weather]

Personalized for you
┌──────────────────────────────┐
│ ❤️ Health & Air Quality      │
│ AQI 138 • UV 6 • Humidity 46%│
│ Moderate air quality...      │
│ Recommendation: ...          │
└──────────────────────────────┘

[Generic weather information]
Hourly
7-Day
etc.

MULTIPLE INTERESTS:

This is critical.

If the user selected:

Health + Fitness

the dashboard must show BOTH personalized insights.

If the user selected:

Travel + Commuting

the dashboard must show BOTH.

If the user selected all four:

Health + Fitness + Travel + Commuting

all four should appear.

Do not show duplicate cards for the same interest.

NO INTEREST FALLBACK:

The onboarding currently requires at least one interest, but make the dashboard safe if the selected interests array is empty.

In that case, simply hide the personalized section or display a small neutral message such as:
"Select your interests to personalize your weather insights."

DESIGN:

Use the existing Step 1 design tokens and dashboard styling.

Personalized cards should visually stand out from generic weather cards, but still feel like part of the same Mausam design system.

Use:
- clear category icon
- strong title
- concise information
- metric badges where useful
- recommendation section
- subtle status styling

Do NOT make the cards huge.
Do NOT fill the dashboard with excessive text.
Do NOT use excessive gradients or glassmorphism.

IMPORTANT PRODUCT REQUIREMENT:

The personalization must be obvious within a few seconds.

A judge should be able to understand:

"These cards exist because I selected these interests."

Therefore display a small contextual line such as:

"Based on your interests: Health & Fitness"

or equivalent.

Do not expose technical terms such as "personalization engine" to the user.

ARCHITECTURE:

Keep responsibilities separated:

src/
├── services/
│   └── personalizationEngine.js
├── components/
│   └── personalized/
│       └── PersonalizedInsightCard.jsx
└── dashboard components...

The engine decides the content.
The component renders the content.
The dashboard decides where the section appears.

Do not unnecessarily modify the existing weather components.

VERIFICATION:

1. Run npm run build.
2. Run the development server.
3. Test these profiles:

TEST A:
Name: Kartik
Location: Jaipur
Interests:
- Health
- Fitness

Expected:
- Health insight visible.
- Fitness insight visible.
- No Travel/Commuting insight.

TEST B:
Change preferences to:
- Travel
- Commuting

Expected:
- Travel insight visible.
- Commuting insight visible.
- Health/Fitness insights hidden.

TEST C:
Select:
- Health
- Fitness
- Travel
- Commuting

Expected:
- All four insights visible.
- No duplicates.

TEST D:
Edit Preferences → change interests → return to dashboard.

Expected:
- Dashboard updates to reflect the new interests.

Also verify:
- existing generic weather sections still work
- hourly forecast still works
- 7-day forecast still works
- alert still works
- browser console has no errors
- responsive layout remains usable

IMPORTANT SCOPE RULE:

STOP after implementing these four personalized categories.

Do NOT implement:
Family
Agriculture
Events
Beach & Surf

Those will be handled in a later step after we inspect this implementation.

REPORT BACK AFTER COMPLETION:

Before stopping, provide a concise but detailed implementation report containing:

1. WHAT YOU DID
- Describe exactly what was implemented.
- Explain how selected interests now affect the dashboard.

2. FILES CHANGED
- List every file created, modified, or deleted.
- For each file, explain its purpose.

3. PERSONALIZATION LOGIC
- Explain the conditions/rules used for Health, Fitness, Travel and Commuting.
- Explain how multiple interests are handled.

4. UI / BEHAVIOR CHANGES
- Describe the new personalized section.
- Explain what happens when interests change.

5. TECHNICAL CHANGES
- Components
- functions
- state/data flow
- imports/dependencies
- any architectural changes

6. VERIFICATION
- Report npm run build result.
- Report dev-server result.
- Report results for TEST A, TEST B, TEST C and TEST D.
- Report responsive/browser testing.
- Report console errors/warnings.

7. DEVIATIONS / ISSUES
- Explicitly state anything that differs from this prompt.
- Mention any assumptions made.

8. CURRENT PROJECT STATE
- What is working now.
- What remains intentionally unimplemented.

STOP HERE.
Do not continue to Family, Agriculture, Events, Beach & Surf, real APIs, or any other feature.