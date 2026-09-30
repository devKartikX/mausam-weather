STEP 23A — MAUSAM TRADEOFF + ARCHITECTURE DECISION AUDIT

IMPORTANT:
ANALYSIS ONLY.
DO NOT MODIFY, CREATE, DELETE, OR REFACTOR ANY CODE.
DO NOT INSTALL DEPENDENCIES.
DO NOT CHANGE THE FRONTEND.
DO NOT CHANGE THE BACKEND.

We have completed:

- React frontend
- FastAPI backend
- real Open-Meteo weather
- real geocoding
- real AQI
- frontend/backend integration
- personalization
- caching
- backend reliability hardening

Before continuing development, we want to resolve the remaining architectural/product tradeoffs.

Your job is to inspect the CURRENT repository and produce a detailed decision report.

==================================================
DECISION 1 — WEATHER PROVIDER
==================================================

Current:
React → FastAPI → Open-Meteo

Investigate the current architecture and determine:

A. What Open-Meteo currently provides to us:
- forecast
- current conditions
- hourly
- daily
- AQI
- limitations

B. What we would gain/lose by integrating IMD as:
1. primary provider
2. secondary provider
3. alerts-only provider
4. future provider

C. Determine whether the current provider abstraction can support IMD later without rewriting the frontend.

IMPORTANT:
Do not implement IMD.

Give a recommendation for the architecture, but clearly separate:
- verified facts
- engineering tradeoffs
- recommendation

==================================================
DECISION 2 — AQI
==================================================

Current:
Open-Meteo provides US EPA AQI.

The UI now explicitly labels:
"Air Quality (US EPA)"

Investigate options for an India-focused AQI source.

Compare:

- current Open-Meteo US AQI
- possible Indian/CPCB-compatible source
- whether IMD provides the necessary AQI data
- data availability
- API accessibility
- reliability
- licensing/usage considerations
- integration complexity

Do not implement anything.

We need a clear answer on whether we should:
A. keep US EPA AQI
B. replace it
C. support multiple AQI standards
D. defer Indian AQI

==================================================
DECISION 3 — OFFICIAL WEATHER ALERTS
==================================================

Current:
alerts = []

Open-Meteo is not being used as the official warning source.

Investigate the official IMD warning/alert ecosystem.

Determine:

- what official warning data is available
- whether there is a usable API/data interface
- what authentication/access requirements exist if known
- whether alerts can be mapped to our current WeatherAlert UI
- whether alerts should be a separate provider/service

Do not implement alerts.

==================================================
DECISION 4 — MARINE / BEACH & SURF
==================================================

Current backend intentionally returns null for:

waveHeight
seaSurfaceTemp
tidalInfo

The product has a Beach & Surf interest category.

Investigate what is realistically required to support:

- wave height
- wave direction
- wave period
- sea surface temperature
- tides

Determine whether:
A. Open-Meteo Marine is sufficient
B. another provider is required
C. tides should remain unsupported
D. Beach & Surf should remain a limited MVP feature

Do not implement marine changes.

==================================================
DECISION 5 — LOCATION SEARCH / AUTOCOMPLETE
==================================================

IMPORTANT NEW PRODUCT REQUIREMENT:

Instead of the current city resolver returning one result, we want city autocomplete.

Example:

User types:

"J"

Suggestions could include:

Jaipur
Jaisalmer
Jalandhar
Jammu
Jamnagar
Jamshedpur
Jhansi
Jodhpur
Junagadh

Each result should ideally display:

City
State/region
Country

Example:

Jaipur
Rajasthan, India

Jodhpur
Rajasthan, India

When the user selects a result, the application should store/use the canonical location including:

city
state
country
latitude
longitude
timezone

Investigate the current LocationService and Open-Meteo geocoding integration.

Determine the best API contract.

For example:

GET /api/location/search?query=J

→ multiple LocationResult objects

instead of:

GET /api/location/search?query=J

→ one LocationResult

Evaluate:

- minimum query length
- maximum number of suggestions
- prefix matching
- relevance/ranking
- duplicate cities
- same city names in different regions
- country/state display
- caching
- provider result limits
- debouncing requirements on frontend
- whether the existing location cache should be reused
- whether selection should store coordinates rather than just city name

IMPORTANT:
Do not implement autocomplete yet.

==================================================
DECISION 6 — LOCATION FALLBACK
==================================================

Current LocationService has known-city fallback behavior.

Audit whether this can ever cause:

User asks for city X
→ geocoder fails
→ backend silently resolves to a different city

Determine whether the current fallback is safe.

Recommend whether to:

A. keep it
B. restrict it to exact canonical city matches
C. remove it
D. use it only as an explicit degraded mode

Do not implement changes.

==================================================
DECISION 7 — CACHE STRATEGY
==================================================

Current:

Weather cache:
15 minutes

Location cache:
24 hours

In-memory.

Evaluate whether we should keep this architecture for the first deployment.

Discuss:

- weather freshness
- AQI freshness
- location freshness
- memory limitations
- multi-instance deployment
- process restarts
- stale data
- future Redis/database implications

Determine whether different weather/AQI TTLs are actually justified.

Do not implement Redis.

==================================================
DECISION 8 — STALE WEATHER FALLBACK
==================================================

Current behavior:

Provider failure
→ error

Consider whether a better production behavior would be:

Fresh provider request fails
↓
recent cached response exists
↓
serve stale cached weather
+
clearly label:
"Updated X minutes ago"

Evaluate:

- user experience
- correctness
- risk of stale weather
- whether this is appropriate for alerts
- whether stale data should be allowed for current weather
- whether stale data should be allowed for AQI
- whether alerts must NEVER be served stale

Do not implement.

==================================================
DECISION 9 — WEATHER FRESHNESS
==================================================

Evaluate whether the current 15-minute weather cache is appropriate.

Do NOT assume:
"provider updates every X minutes"

Instead distinguish:

- provider/model update cadence
- our cache policy
- user-facing freshness

Determine whether the product needs:

- one TTL
- separate TTLs
- background refresh
- request-time refresh

Do not implement.

==================================================
DECISION 10 — LOCALSTORAGE VS ACCOUNTS
==================================================

Current:

User preferences → localStorage

No authentication/database.

Evaluate:

MVP:
localStorage

Future:
account
→ database
→ cross-device preferences

Determine when accounts actually become necessary.

Do not implement authentication.

==================================================
DECISION 11 — DEVELOPMENT VS PRODUCTION NETWORKING
==================================================

Current development:

React :3000
↓
Vite proxy
↓
FastAPI :8000

Determine the clean production architecture.

Evaluate:

- frontend hosting
- backend hosting
- HTTPS
- CORS
- API URL configuration
- reverse proxy
- containerization
- process supervision

Do not deploy.

Do not modify Vite configuration.

==================================================
DECISION 12 — SIH PRODUCT REQUIREMENTS
==================================================

Review the current product against the original SIH problem:

"Development of personalized homepage for 'Mausam' mobile application"

Determine which of the following are:

MUST HAVE
SHOULD HAVE
NICE TO HAVE
DEFER

Consider:

- real weather
- personalization
- location search
- AQI
- alerts
- marine
- accounts
- notifications
- deployment
- accessibility
- mobile experience

Do not invent requirements not supported by the project context.

==================================================
FINAL ARCHITECTURE RECOMMENDATION
==================================================

After analyzing all decisions, propose a target architecture.

Show:

CURRENT:

React
 ↓
FastAPI
 ↓
Open-Meteo

TARGET:

React
 ↓
API layer
 ↓
Weather service
 ├── weather provider
 ├── AQI provider
 ├── alerts provider
 ├── marine provider
 └── location provider
 ↓
normalized schemas

Also show which providers should actually be implemented now versus later.

==================================================
IMPLEMENTATION ORDER
==================================================

Provide a recommended implementation sequence AFTER this audit.

It should explicitly identify:

1. what must be changed before UI/UX work
2. what can be changed during UI/UX work
3. what should wait until deployment
4. what should wait until after deployment/accounts

==================================================
MANDATORY REPORT

Report:

1. Current architecture assessment
2. Weather provider tradeoff
3. AQI tradeoff
4. Official alerts tradeoff
5. Marine tradeoff
6. Location autocomplete design
7. Location fallback assessment
8. Cache tradeoff
9. Stale-data fallback assessment
10. Freshness assessment
11. LocalStorage/accounts tradeoff
12. Production networking assessment
13. SIH requirement classification
14. Recommended target architecture
15. Recommended provider strategy
16. Recommended implementation order
17. Decisions that require human/product approval
18. Risks
19. Assumptions
20. Anything you could not verify

IMPORTANT:
Do not modify any files.

ANALYSIS ONLY.

STOP after the report.