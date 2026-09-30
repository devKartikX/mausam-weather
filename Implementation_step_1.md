IMPLEMENTATION STEP 1 — PROJECT FOUNDATION ONLY

We have completed the analysis of SIH 2026 Problem Statement 26076:
“Development of personalized homepage for ‘Mausam’ mobile application.”

You have already analyzed the PS and proposed the architecture.

Now implement ONLY the project foundation.

IMPORTANT:
This is Step 1 of a controlled, incremental implementation.
Do NOT build the onboarding page yet.
Do NOT build the dashboard yet.
Do NOT build personalized cards yet.
Do NOT build the personalization engine yet.
Do NOT add authentication.
Do NOT add signup/login.
Do NOT add a database.
Do NOT add real weather APIs.
Do NOT add the persona switcher yet.

==================================================
PROJECT GOAL — KEEP THIS IN MIND
==================================================

The final application will be a personalized Mausam weather experience.

The final user flow will be:

User opens application
        ↓
Enters name
        ↓
Enters/selects city
        ↓
Selects one or more interests
        ↓
Create My Dashboard
        ↓
Personalized weather homepage
        ↓
Weather information is prioritized according to interests

The final application should demonstrate that different users receive different weather information based on what matters to them.

Possible interests:

- Health
- Fitness
- Travel
- Family
- Agriculture
- Commuting
- Events
- Beach & Surf

The final UI must be polished, modern, responsive, simple to understand, and suitable for an SIH prototype demonstration.

==================================================
1. INSPECT THE CURRENT PROJECT
==================================================

Before making changes:

- Inspect the current workspace.
- Determine whether React/Vite is already initialized.
- Check package.json if present.
- Check existing configuration.
- Do NOT unnecessarily recreate or delete an existing working setup.

The workspace currently contains the SIH problem-analysis material but no completed application.

==================================================
2. TECHNOLOGY
==================================================

Use:

- React
- Vite
- JavaScript/JSX unless the existing project is already configured differently
- CSS

Prefer a simple frontend architecture.

Do NOT introduce unnecessary frameworks or libraries.

If an icon library is needed, use Lucide React.

Do not install libraries merely for visual effects.

==================================================
3. CREATE THE BASIC PROJECT STRUCTURE
==================================================

Establish a clean structure that can support the final application.

Use this as the intended structure:

src/
├── assets/
├── components/
│   ├── common/
│   ├── onboarding/
│   ├── dashboard/
│   └── personalized/
├── data/
├── services/
├── utils/
├── styles/
├── App.jsx
└── main.jsx

Do not create dozens of empty component files.

Only create directories/files that are actually required at this stage.

Future responsibilities:

components/common/
- reusable UI elements

components/onboarding/
- name/location/interests setup UI

components/dashboard/
- weather dashboard components

components/personalized/
- interest-specific weather cards

data/
- interests and later mock weather data

services/
- later weather-data abstraction and personalization logic

utils/
- small reusable helper functions

styles/
- global styles and design tokens

==================================================
4. GLOBAL DESIGN SYSTEM
==================================================

Create the basic visual foundation now.

Define reusable CSS variables/tokens for:

- Primary background
- Secondary background
- Card background
- Primary text
- Secondary text
- Muted text
- Border
- Accent
- Success
- Warning
- Danger
- Border radius
- Shadows
- Spacing
- Typography

The final design should feel like a modern premium weather application.

Design direction:

- Clean
- Minimal
- Professional
- Spacious
- Modern
- Soft rounded corners
- Subtle shadows
- Strong visual hierarchy
- Weather-inspired but not childish
- Avoid excessive glassmorphism
- Avoid excessive gradients
- Avoid excessive animations

The interface must remain easy to read.

==================================================
5. RESPONSIVE FOUNDATION
==================================================

Set up responsive styling for:

- Mobile
- Tablet
- Desktop

Use a mobile-first approach where practical.

The final application must work well on a phone-sized screen because Mausam is a mobile application concept.

Do not create separate desktop/mobile applications.

Use responsive layouts.

==================================================
6. APPLICATION SHELL
==================================================

Create only the basic App structure.

App should currently render a simple temporary placeholder indicating:

“Mausam”

and:

“Personalized Weather Experience”

This placeholder exists ONLY to verify that the application foundation works.

Do not build the actual onboarding screen yet.

==================================================
7. CODE QUALITY
==================================================

Keep the architecture simple.

Requirements:

- Functional React components
- Clear naming
- No unnecessary abstraction
- No duplicated global styles
- No huge monolithic component
- Keep UI components reusable
- Keep data separate from UI
- Keep future API integration separate from UI

Do not add functionality that has not been requested.

==================================================
8. FUTURE ARCHITECTURE — DO NOT IMPLEMENT YET
==================================================

Keep the architecture ready for these future parts:

A. User profile:

{
  name,
  location,
  interests
}

B. Mock weather data:

- Current temperature
- Condition
- Feels-like
- High/Low
- Humidity
- Wind
- UV
- AQI
- Rain probability
- Visibility
- Hourly forecast
- Daily forecast
- Relevant specialized weather information

C. Personalization:

Selected interests determine which information/cards appear.

D. Future real data:

The mock data layer should eventually be replaceable by real weather/IMD data without rewriting the UI.

But NONE of these features should be implemented in this step.

==================================================
9. DO NOT OVER-ENGINEER
==================================================

This is a prototype.

Do NOT create:

- Authentication
- Login
- Signup
- Database
- Backend server
- ML model
- AI API
- Weather API
- State management library
- Complex routing system
- Cloud infrastructure
- Deployment configuration
- Persona switcher

unless something already exists and is required by the current project.

We will add functionality incrementally in later steps.

==================================================
10. VERIFICATION
==================================================

After implementation:

- Run the development server.
- Confirm the application starts successfully.
- Confirm there are no build errors.
- Confirm there are no console errors caused by your changes.
- Confirm the basic placeholder renders.
- Confirm the responsive foundation does not produce obvious layout problems.

==================================================
11. FINAL RESPONSE
==================================================

After completing this step, report:

1. What files/directories you created.
2. What existing files you changed.
3. What dependencies you installed, if any.
4. What design foundation was established.
5. How you verified the application.
6. Any issues or decisions that need my approval.

IMPORTANT:

STOP after this foundation step.

Do NOT continue automatically to onboarding, dashboard, weather data, or personalization.

Wait for my next instruction.