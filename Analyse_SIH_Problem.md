We are building a prototype for SIH 2026 Problem Statement 26076:

“Development of personalized homepage for ‘Mausam’ mobile application”

Before writing ANY code or creating/modifying ANY files, I want you to carefully analyze the problem statement and understand the product we are supposed to build.

IMPORTANT:
- Do NOT start implementation yet.
- Do NOT create files yet.
- Do NOT install packages yet.
- Do NOT modify the existing project.
- Your job in this step is ONLY analysis and planning.
- Wait for my explicit command before implementing anything.

==================================================
1. UNDERSTAND THE PROBLEM
==================================================

The problem is about creating a personalized homepage for the “Mausam” weather application.

The important idea is NOT simply displaying normal weather information.

The homepage should understand what information is relevant to a particular user based on their interests and lifestyle.

Different users need different weather information.

Examples from the problem statement:

Health-conscious users may care about:
- AQI
- Pollen
- UV index
- Humidity
- Health-related weather conditions

Outdoor fitness users may care about:
- Sunrise/sunset
- Best time for running/exercise
- Wind speed
- Temperature
- UV
- Heat/rain alerts

Travelers may care about:
- Weather conditions
- Severe weather alerts
- Saved destinations
- Rain probability
- Packing suggestions

Parents/families may care about:
- School commute conditions
- Rain alerts
- Severe weather warnings

Agriculture/gardening users may care about:
- Rainfall
- Soil moisture
- Humidity
- Frost/heat conditions
- Planting/gardening guidance

Commuters may care about:
- Visibility
- Fog
- Rain
- Storms
- Conditions affecting travel

Event planners may care about:
- Extended forecast
- Rain probability
- Temperature
- Humidity
- Outdoor comfort

Beach/surf users may care about:
- Wave height
- Tide
- Water temperature
- Wind
- Sea conditions

The core problem is therefore:

“How can we show each user the weather information that matters most to them instead of showing every user the same generic weather dashboard?”

==================================================
2. OUR PRODUCT CONCEPT
==================================================

We are building a FRONTEND-FIRST prototype of this personalized Mausam experience.

We are intentionally keeping the prototype simple because the immediate goal is to demonstrate the concept clearly through a polished and functional UI.

There will be NO:
- Login
- Signup
- Password
- Authentication
- User account system
- Complex database
- Machine learning model
- Complex backend
- Complicated infrastructure

The prototype will use realistic mock weather data.

The architecture should, however, be clean enough that real weather APIs and a backend can be added later.

==================================================
3. USER FLOW
==================================================

The basic flow should be:

USER OPENS APPLICATION
        ↓
PERSONALIZATION SCREEN
        ↓
User enters:
- Name
- Location/city
- Interests
        ↓
User selects one or multiple interests
        ↓
User clicks “Create My Dashboard”
        ↓
PERSONALIZATION LOGIC
        ↓
PERSONALIZED WEATHER DASHBOARD

The dashboard should use the user's selected interests to determine which personalized weather information/cards are displayed.

Example:

User:
Name = Kartik
Location = Jaipur
Interests = Fitness + Health

Dashboard should prioritize:
- Current weather
- Temperature
- AQI
- UV index
- Humidity
- Wind
- Best running time
- Fitness recommendation
- Health recommendation
- Relevant alerts

Another user might select:

Travel + Commuting

Their dashboard should prioritize different information.

==================================================
4. WHAT THE APPLICATION SHOULD DEMONSTRATE
==================================================

The most important thing the prototype must communicate is:

“MAUSAM DOES NOT SHOW THE SAME WEATHER INFORMATION TO EVERY USER.”

Instead:

USER PROFILE
    ↓
USER INTERESTS
    ↓
PERSONALIZATION
    ↓
RELEVANT WEATHER INFORMATION

This personalization is the main feature of the project.

The UI should make this immediately understandable to a judge.

==================================================
5. FRONTEND PRIORITY
==================================================

This is a prototype for an SIH submission.

Prioritize:

1. Visual quality
2. User experience
3. Personalization concept
4. Working interactions
5. Clean architecture

Backend complexity is intentionally low.

Use mock data initially.

The application should look like a serious modern weather application rather than a basic college CRUD project.

==================================================
6. INITIAL PAGE CONCEPT
==================================================

The first page is NOT a signup page.

It is a simple personalization/welcome page.

It should ask:

“What’s your name?”

“What city are you in?”

“What are you interested in?”

The user can select multiple interests.

Possible interests:

- Health
- Fitness
- Travel
- Family
- Agriculture
- Commuting
- Events
- Beach & Surf

Then:

“Create My Dashboard”

The application uses these selections to construct the personalized dashboard.

==================================================
7. MAIN DASHBOARD CONCEPT
==================================================

The main dashboard should contain:

A. Personalized greeting
Example:

“Good evening, Kartik 👋”

“Here’s your personalized weather for Jaipur.”

B. Current weather
- Location
- Temperature
- Weather condition
- Weather icon
- Feels-like temperature
- High/Low
- Humidity
- Wind

C. Forecast
- Hourly forecast
- Multi-day forecast

D. Personalized information

This section changes depending on selected interests.

E. Weather alerts
Examples:
- Rain expected this evening
- High UV during afternoon
- Strong winds
- Fog/visibility warning
- Severe weather warning

F. Personalized recommendations

Examples:
- Best time for outdoor exercise
- Carry an umbrella
- Good conditions for outdoor events
- Poor visibility during commute
- etc.

==================================================
8. PERSONALIZATION LOGIC
==================================================

The personalization system does NOT need AI or ML.

Use simple deterministic logic.

Conceptually:

if user selects Fitness:
    show fitness-related weather information

if user selects Health:
    show health-related weather information

if user selects Travel:
    show travel-related weather information

etc.

Multiple interests should work simultaneously.

For example:

Fitness + Health

should display both Fitness and Health insight cards.

==================================================
9. DATA STRATEGY
==================================================

Use mock weather data for the prototype.

Keep weather data separate from UI components.

The structure should be designed so that later:

Mock Weather Data
        ↓
can become
        ↓
Real Weather API / IMD Data

without requiring a complete rewrite of the frontend.

==================================================
10. WHAT I WANT YOU TO DO NOW
==================================================

DO NOT IMPLEMENT ANYTHING YET.

First inspect the existing project structure and determine what already exists.

Then provide me with a proposed project architecture.

Your response should include:

1. Your understanding of the problem statement.
2. The exact product we are going to build.
3. The complete user flow.
4. Major frontend sections/pages.
5. Major reusable components.
6. Data/model structures we will need.
7. Personalization logic structure.
8. Proposed folder structure.
9. What files you recommend creating.
10. What existing files should be reused.
11. Which parts are mock data.
12. Which parts can later be connected to real APIs.
13. Recommended implementation order.

For the folder structure, propose something similar to:

src/
├── components/
├── pages/
├── data/
├── hooks/
├── utils/
├── styles/
└── ...

But DO NOT blindly use this structure.
Choose the structure based on the existing project.

IMPORTANT:
Do not create or modify anything yet.

After presenting the analysis and proposed architecture, STOP and wait for my next instruction.