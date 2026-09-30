STEP 31 — PRODUCTION DEPLOYMENT OF MAUSAM

OBJECTIVE

The Mausam application has completed:

- Backend/data implementation
- Real weather integration
- Location/autocomplete implementation
- AQI integration
- IMD/Sachet alert integration
- Marine integration
- Cache/stale-data handling
- Timezone handling
- UI/UX polish
- Full end-to-end QA

Step 30 final QA marked the application:

READY FOR DEPLOYMENT

This task is now the production deployment phase.

TARGET DEPLOYMENT ARCHITECTURE:

GitHub
   ↓
Render
   ├── React/Vite frontend → Static Site
   └── FastAPI backend     → Web Service
                                  ↓
                         Open-Meteo
                         Sachet/NDMA/IMD
                         other providers

The goal is to produce a working public HTTPS deployment with the frontend correctly communicating with the production FastAPI backend.

IMPORTANT:

This is a production deployment task.

Do NOT redesign the UI.

Do NOT change personalization behavior.

Do NOT change weather-provider logic unless required to make production deployment work.

Do NOT add authentication.

Do NOT add a database.

Do NOT add new product features.

Do NOT replace real APIs with mocks.

Do NOT put secrets/API keys into Git.

Do NOT commit .env files containing secrets.

Do NOT expose backend provider credentials to React.

Do NOT silently change working application behavior.

If a deployment action requires an account login, OAuth approval, domain ownership, secret, or manual browser action that you cannot perform, STOP at that exact point and report the exact action required from me. Do not guess credentials or fake successful deployment.

--------------------------------------------------
PART 1 — COMPLETE REPOSITORY AUDIT
--------------------------------------------------

Before changing anything, inspect the entire repository.

Inspect:

package.json
vite.config.*
src/
backend/
backend/requirements.txt
backend/main.py
backend/api/
backend/services/
backend/schemas/
.gitignore
README*
any existing deployment/configuration files
any .env files
any example environment files
PROGRESS.md
architecture/documentation files if present

Determine:

1. Frontend build command.
2. Frontend output directory.
3. Backend startup command.
4. Backend Python version requirements.
5. Backend dependency installation method.
6. Current CORS configuration.
7. Current frontend API URL/proxy configuration.
8. All environment variables used by frontend.
9. All environment variables used by backend.
10. Any hardcoded localhost URLs.
11. Any hardcoded 127.0.0.1 URLs.
12. Any production-incompatible development settings.
13. Any secrets or credentials accidentally present in the repository.

DO NOT deploy yet.

--------------------------------------------------
PART 2 — GIT SAFETY AUDIT
--------------------------------------------------

Before pushing anything to GitHub, inspect:

git status

git branch

git remote -v

git log --oneline -10

Inspect .gitignore carefully.

The repository MUST NOT commit:

node_modules/
.venv/
.env
.env.*
!.env.example
__pycache__/
*.pyc
dist/
build/
coverage/
Playwright/Puppeteer generated artifacts
OS metadata
IDE-specific temporary files
logs
local cache files
credentials
API keys
private certificates
private deployment files

Do NOT blindly add everything.

Check tracked files for possible secrets.

Search for patterns such as:

API_KEY
APIKEY
SECRET
PASSWORD
TOKEN
PRIVATE_KEY
ACCESS_KEY

Also inspect:

git diff
git diff --cached

If any real credential is discovered:

STOP.

Do not push it.

Report the exact file and required remediation.

Never print the actual secret value in the final report.

--------------------------------------------------
PART 3 — CREATE SAFE ENVIRONMENT CONFIGURATION
--------------------------------------------------

Production configuration must use environment variables.

Do NOT hardcode production URLs into source code if an environment variable is appropriate.

Create/update a safe example configuration if needed:

.env.example

This file may contain variable names and placeholder values only.

For example:

VITE_API_BASE_URL=

Do NOT put actual production secrets in .env.example.

If the backend currently needs no secret environment variables, document that clearly.

--------------------------------------------------
PART 4 — FIX FRONTEND PRODUCTION API CONFIGURATION
--------------------------------------------------

Current development architecture uses Vite proxy:

Frontend
→ /api
→ 127.0.0.1:8000

That is fine locally but MUST NOT be relied upon in production.

Implement a production-safe configuration.

The frontend should support:

Development:

VITE_API_BASE_URL=http://127.0.0.1:8000

Production:

VITE_API_BASE_URL=<PRODUCTION_BACKEND_URL>

The production URL must be supplied through the deployment environment.

Do not hardcode an unknown production URL.

The frontend must continue to work locally.

Verify:

Development:
frontend → local FastAPI

Production:
frontend → HTTPS production FastAPI

Do NOT make React call Open-Meteo, Sachet, or other external providers directly.

All provider calls must remain backend-side.

--------------------------------------------------
PART 5 — AUDIT weatherClient.js AND locationClient.js
--------------------------------------------------

Inspect:

src/services/weatherClient.js
src/services/locationClient.js

Ensure both correctly construct production requests.

Requirements:

- no localhost in production
- no 127.0.0.1 in production
- no direct provider URLs
- no API keys
- no hardcoded development-only assumptions
- errors remain user-friendly

Be careful about paths.

Production frontend requests should resolve correctly to:

<PRODUCTION_BACKEND_URL>/api/weather
<PRODUCTION_BACKEND_URL>/api/location/search

Do not accidentally produce:

<PRODUCTION_BACKEND_URL>/api/api/weather

or missing `/api`.

Test the resulting URLs.

--------------------------------------------------
PART 6 — BACKEND PRODUCTION CONFIGURATION
--------------------------------------------------

Inspect backend/main.py and current server configuration.

The FastAPI backend must be runnable by a production hosting platform.

Do not use:

uvicorn --reload

in production.

Production startup must be equivalent to:

uvicorn backend.main:app --host 0.0.0.0 --port $PORT

Use the hosting platform's PORT environment variable.

Do not hardcode port 8000 for production.

Keep local development behavior working.

--------------------------------------------------
PART 7 — CORS PRODUCTION CONFIGURATION
--------------------------------------------------

Current CORS is restricted to local development origins.

Production requires the deployed frontend origin.

Implement environment-based CORS.

Development should allow:

http://localhost:3000
http://127.0.0.1:3000

Production should allow ONLY the actual deployed frontend HTTPS origin.

Do NOT use:

allow_origins=["*"]

Do NOT enable unnecessary credentials.

Keep:

allow_credentials=False

unless the existing application genuinely requires credentials.

Do not invent a production domain.

The actual Render frontend URL must be inserted through the appropriate deployment configuration after it is known.

If frontend and backend URLs are not yet known, use environment configuration rather than hardcoding placeholders into production code.

--------------------------------------------------
PART 8 — HEALTH ENDPOINT
--------------------------------------------------

Verify:

/api/health

works without requiring:

- external weather provider
- location provider
- AQI provider
- alert provider
- marine provider

The health endpoint must remain lightweight.

This will be used to verify the production backend is alive.

--------------------------------------------------
PART 9 — PRODUCTION DEPENDENCIES
--------------------------------------------------

Inspect:

backend/requirements.txt

Verify all runtime dependencies are explicitly listed and pinned appropriately.

Do not include unnecessary development dependencies.

Ensure the production platform can install them from requirements.txt.

Verify:

fastapi
uvicorn
httpx
and all actual runtime dependencies

are present.

Do not remove required dependencies.

--------------------------------------------------
PART 10 — PYTHON VERSION COMPATIBILITY
--------------------------------------------------

Determine the Python version used successfully during local QA.

Create the appropriate Render Python runtime configuration if required.

Do NOT arbitrarily upgrade Python.

Use the version known to work with the current project.

If the project requires a specific version, document it.

--------------------------------------------------
PART 11 — FRONTEND BUILD CONFIGURATION
--------------------------------------------------

Verify:

npm install
npm run build

works from a clean environment.

Determine:

- build command
- output directory
- required Node version

If Node version needs to be pinned, add an appropriate configuration such as:

engines

or the platform-specific configuration supported by the repository.

Do not upgrade dependencies unnecessarily.

Do not change React/Vite versions unless deployment genuinely requires it.

--------------------------------------------------
PART 12 — RENDER DEPLOYMENT PLAN
--------------------------------------------------

Use two Render services:

SERVICE 1:
Mausam Backend

Type:
Web Service

Runtime:
Python

Build command:
pip install -r backend/requirements.txt

Start command:
uvicorn backend.main:app --host 0.0.0.0 --port $PORT

Root directory:
repository root unless the repository structure requires another directory.

SERVICE 2:
Mausam Frontend

Type:
Static Site

Build command:

npm install && npm run build

Publish directory:

dist

If the existing repository structure requires different commands, inspect first and use the correct commands rather than blindly applying these.

--------------------------------------------------
PART 13 — GITHUB REPOSITORY
--------------------------------------------------

Before deployment, ensure the complete tested project is committed.

First show:

git status

Then verify:

- correct branch
- correct remote
- no secrets
- no .env
- no node_modules
- no .venv
- no build artifacts
- no temporary files
- no test credentials

Then create a meaningful commit.

Example:

git add .
git commit -m "Prepare Mausam for production deployment"

Do not push yet if secrets or repository issues remain.

After verifying the commit:

git push

If the repository does not yet have a remote:

STOP and report:

- current branch
- repository state
- exact GitHub setup action required

Do not invent a GitHub repository URL.

--------------------------------------------------
PART 14 — VERIFY GITHUB AFTER PUSH
--------------------------------------------------

After push, verify:

- commit exists on remote
- expected files exist
- no secrets were committed
- frontend source exists
- backend source exists
- requirements.txt exists
- .gitignore exists
- deployment configuration exists if used

Do not assume a successful local git push means the repository is correct.

--------------------------------------------------
PART 15 — CREATE RENDER BACKEND
--------------------------------------------------

Create the backend Render Web Service.

Use the GitHub repository.

Configure:

Name:
mausam-backend

Environment:
Python

Build:
pip install -r backend/requirements.txt

Start:
uvicorn backend.main:app --host 0.0.0.0 --port $PORT

Do not use --reload.

Set required environment variables.

At minimum verify:

PORT

Do not manually set PORT unless Render requires it.

Configure any other required environment variables discovered during the audit.

Do not create fake values.

--------------------------------------------------
PART 16 — BACKEND DEPLOYMENT VERIFICATION
--------------------------------------------------

After Render backend deployment completes, obtain the actual HTTPS backend URL.

Example format only:

https://<actual-backend>.onrender.com

Do not hardcode this example.

Test:

<backend-url>/api/health

Expected:

HTTP 200

Then test:

/api/location/search

with:

Jaipur
Mumbai
London

Then test:

/api/weather

with:

Jaipur
Mumbai
London

Verify:

- HTTP 200 where expected
- normalized response
- no traceback
- no provider credential issue
- no CORS issue at backend level
- real weather data
- AQI
- marine behavior
- alerts behavior
- timezone

If backend deployment fails:

STOP and diagnose the actual error before proceeding.

Do not proceed to frontend deployment while the backend is broken.

--------------------------------------------------
PART 17 — CONFIGURE PRODUCTION CORS
--------------------------------------------------

Once the actual frontend URL is known, update backend production configuration to allow ONLY that frontend origin.

Example:

https://<actual-frontend>.onrender.com

Do not include example domains.

Do not use wildcard CORS.

Redeploy backend after changing CORS.

Verify CORS using an actual browser request from the deployed frontend.

--------------------------------------------------
PART 18 — CREATE RENDER FRONTEND
--------------------------------------------------

Create:

mausam-frontend

Type:

Static Site

Build:

npm install && npm run build

Publish directory:

dist

Set:

VITE_API_BASE_URL=<ACTUAL_BACKEND_HTTPS_URL>

Do not put the backend URL directly into source code if environment configuration is available.

IMPORTANT:

Vite environment variables beginning with VITE_ are bundled into the frontend.

Therefore:

ONLY put public configuration such as the backend base URL there.

NEVER put:

API keys
private tokens
passwords
secrets

in VITE_* variables.

--------------------------------------------------
PART 19 — FRONTEND DEPLOYMENT VERIFICATION
--------------------------------------------------

After deployment, open the actual public frontend URL.

Verify:

- page loads over HTTPS
- no blank page
- no build errors
- no console errors
- no failed API requests
- frontend successfully contacts production backend

Open browser DevTools and verify API calls go to:

actual HTTPS backend

NOT:

127.0.0.1
localhost
development Vite server
Open-Meteo directly

--------------------------------------------------
PART 20 — LIVE USER FLOW
--------------------------------------------------

Test the actual deployed website from a clean browser/incognito session.

Complete:

Onboarding
→ Name
→ Location
→ Interests
→ Dashboard

Verify:

weather loads.

Then test:

Jaipur
Mumbai
Bengaluru
Delhi
Chennai
London

Verify:

- current weather
- hourly
- daily
- AQI
- UV
- sunrise/sunset
- alerts
- marine
- personalization
- timezone
- updated time

--------------------------------------------------
PART 21 — LIVE AUTOCOMPLETE
--------------------------------------------------

On the deployed website test:

J
Ja
Jai
M
Mum
Mumbai
Lon
London
xyzrandom999

Verify:

- J returns valid local fallback results
- Ja ranks Jaipur appropriately
- Jai ranks Jaipur first
- Mum ranks Mumbai first
- Lon ranks London first
- unknown query gives empty state
- keyboard navigation works
- Escape works
- selection works

--------------------------------------------------
PART 22 — LIVE ALERT TEST
--------------------------------------------------

Verify the deployed application correctly handles:

1. Active warning.
2. No active warning.
3. Warning service unavailable.

Verify the UI never displays raw provider JSON.

Verify source attribution remains visible.

Do not fabricate an alert merely to make the deployment test pass.

--------------------------------------------------
PART 23 — LIVE MARINE TEST
--------------------------------------------------

Test:

Mumbai
Chennai
Jaipur
Bengaluru

Verify:

Mumbai/Chennai:
real wave data where available.

Jaipur/Bengaluru:
graceful inland handling.

Do not display fake tides or SST.

--------------------------------------------------
PART 24 — LIVE STALE WEATHER TEST
--------------------------------------------------

If practical without damaging production data, verify stale behavior.

Do NOT manipulate the production cache destructively.

If direct simulation is not safe on the deployed service:

- verify the stale implementation in the tested codebase
- verify the production metadata contract
- document that destructive provider-failure simulation was not performed against production

Never intentionally break production just to test failure behavior.

--------------------------------------------------
PART 25 — LIVE RESPONSIVE TEST
--------------------------------------------------

Test the deployed URL at:

320px
360px
390px
430px
768px
1024px
1440px

Verify:

- no horizontal overflow
- no broken layout
- no clipped cards
- location dropdown works
- weather cards work
- scrolling works
- touch targets remain usable

--------------------------------------------------
PART 26 — PERFORMANCE CHECK
--------------------------------------------------

Check the deployed application for obvious problems:

- extremely slow first load
- repeated API requests
- request loops
- failed provider requests
- unnecessary reloads
- console errors
- broken static assets

Do not prematurely optimize.

Only fix actual deployment problems.

--------------------------------------------------
PART 27 — HTTPS AND SECURITY
--------------------------------------------------

Verify:

Frontend uses HTTPS.

Backend uses HTTPS.

No mixed-content errors.

No API keys are exposed.

No secrets appear in:

- frontend source
- browser network payloads
- browser localStorage
- browser console
- GitHub repository

Verify production CORS is restricted.

Verify no development server is exposed publicly.

--------------------------------------------------
PART 28 — RENDER SLEEP / COLD START
--------------------------------------------------

If the selected Render plan may sleep when idle, test the first request after inactivity.

Verify the application eventually loads correctly.

Do not treat normal cold-start latency as a functional failure.

Document the behavior if relevant.

Do not add unnecessary infrastructure just to solve cold starts unless required.

--------------------------------------------------
PART 29 — DEPLOYMENT DOCUMENTATION
--------------------------------------------------

Update README.md with a concise production section containing:

- project overview
- frontend
- backend
- local development
- environment variables
- production architecture
- deployment services
- health endpoint
- important security notes

Do NOT put:

- secrets
- private URLs
- tokens
- passwords

in README.

If actual public frontend/backend URLs are safe and intended to be public, document them.

Otherwise leave placeholders.

--------------------------------------------------
PART 30 — PRODUCTION GIT COMMIT
--------------------------------------------------

After successful deployment configuration and verification:

Run:

git status

Review every changed file.

Then:

git diff

Verify no:

- secrets
- .env
- credentials
- unnecessary generated files
- deployment logs

Then commit deployment configuration.

Example:

git add .
git commit -m "Deploy Mausam production configuration"

Then:

git push

Verify the remote branch is up to date.

--------------------------------------------------
PART 31 — DO NOT DESTROY LOCAL DEVELOPMENT
--------------------------------------------------

After production deployment, verify local development still works.

Run:

npm install

backend environment setup

npm run build

local frontend

local FastAPI

Verify local API proxy still works.

Do not replace development configuration with production-only values.

Development and production must coexist.

--------------------------------------------------
PART 32 — FINAL LIVE SMOKE TEST
--------------------------------------------------

Perform one final real-user test:

1. Open production URL.
2. Start with clean browser state.
3. Complete onboarding.
4. Search location.
5. Select interests.
6. Open dashboard.
7. Wait for real weather.
8. Check personalized cards.
9. Change location.
10. Verify updated weather.
11. Test autocomplete.
12. Check AQI.
13. Check alerts.
14. Check marine if coastal.
15. Refresh.
16. Verify profile persistence.
17. Check mobile layout.
18. Check browser console.

Only after all of these pass should deployment be considered successful.

--------------------------------------------------
PART 33 — FINAL DEPLOYMENT REPORT
--------------------------------------------------

Provide a detailed final report containing:

GIT

1. Git repository status
2. Branch used
3. Commit hash
4. Confirmation that push succeeded
5. Confirmation that no secrets were committed

FRONTEND

6. Frontend deployment platform
7. Frontend production URL
8. Build command
9. Publish directory
10. Production environment variables

BACKEND

11. Backend deployment platform
12. Backend production URL
13. Backend start command
14. Backend health endpoint result
15. Backend environment variables

NETWORKING

16. Production CORS configuration
17. HTTPS status
18. Confirmation no localhost/127.0.0.1 production dependency remains

LIVE TESTING

19. Onboarding result
20. Location/autocomplete result
21. Weather result
22. AQI result
23. Alert result
24. Marine result
25. Personalization result
26. Timezone result
27. City-switch result
28. Persistence result
29. Responsive result
30. Browser console result

SECURITY

31. Secret scan result
32. Frontend API-key scan result
33. Direct-provider-call scan result

PRODUCTION

34. Cold-start behavior
35. Performance observations
36. Any remaining production limitations

FINAL VERDICT

Choose exactly one:

DEPLOYMENT SUCCESSFUL

or

DEPLOYMENT BLOCKED

If blocked:

- clearly state the exact blocker
- show the relevant error
- explain what manual action is required
- DO NOT claim deployment succeeded

--------------------------------------------------
CRITICAL STOP CONDITIONS
--------------------------------------------------

STOP immediately if:

- credentials are required and unavailable
- GitHub authentication is required and unavailable
- Render authentication is required and unavailable
- deployment fails
- build fails
- backend fails to start
- frontend cannot reach backend
- CORS fails
- secrets are discovered
- production configuration is ambiguous

Do not guess.

Do not fabricate successful deployment.

Do not bypass security.

Do not commit secrets.

If a manual action is required, tell me exactly what I need to click/type/do, then STOP.

If deployment succeeds, do NOT start adding new features.

The deployment phase is complete only after the final live smoke test and final report.