STEP 16 — ANALYZE AND SELECT THE REAL GEOCODING PROVIDER

IMPORTANT:
THIS IS AN ANALYSIS-ONLY STEP.

Do NOT modify any files.
Do NOT install dependencies.
Do NOT create provider implementations.
Do NOT make permanent code changes.
Do NOT modify the frontend.
Do NOT connect any external API.

We need to choose the real geocoding provider before implementation.

OBJECTIVE

Evaluate realistic geocoding options for this project and recommend an implementation path that is suitable for:

- a deployed web/mobile-style weather product
- Indian cities and major global cities
- city-level weather
- coordinates + timezone
- reasonable reliability
- caching
- rate limiting
- future growth
- development/demo usage
- eventual production deployment

CURRENT CONTRACT

Our backend already has:

GET /api/location/search?query=...

and:

LocationResult:
- city
- state
- country
- latitude
- longitude
- timezone
- displayName

The future provider must be adapted into this contract.

CANDIDATES TO EVALUATE

At minimum investigate:

1. Open-Meteo Geocoding API
2. Public Nominatim / OpenStreetMap geocoding
3. At least one realistic production/commercial geocoding alternative

For the commercial alternative, select an appropriate provider such as:
- Google Maps Geocoding
- Mapbox Search/Geocoding
- Geoapify
- another credible provider

Do not assume a provider is suitable merely because it has a free tier.

EVALUATE EACH PROVIDER ON:

1. API availability
2. Terms/licensing
3. Free-tier restrictions
4. Commercial-use restrictions
5. Rate limits
6. Required API keys
7. User-Agent/attribution requirements
8. Global city coverage
9. India coverage
10. Timezone availability
11. Coordinate accuracy
12. Response quality
13. Search behavior for city names
14. Infrastructure/reliability
15. Caching suitability
16. Ease of FastAPI integration
17. Cost implications
18. Suitability for an SIH/demo environment
19. Suitability for eventual deployment
20. Whether the provider can be replaced later without frontend changes

IMPORTANT:

Distinguish clearly between:

A. Facts verified from official provider documentation
B. Your engineering assessment
C. Assumptions that still require verification

Do not make unsupported claims.

NOMINATIM-SPECIFIC REQUIREMENT

If evaluating public Nominatim, explicitly inspect its current official usage policy.

Pay particular attention to:
- request-rate limits
- caching
- User-Agent/Referer
- attribution
- autocomplete restrictions
- production/commercial suitability

OPEN-METEO-SPECIFIC REQUIREMENT

Inspect current official Open-Meteo geocoding documentation and terms.

Determine:
- what the free API permits
- whether commercial use is permitted
- rate limits
- attribution requirements
- API key requirements
- whether its geocoding response contains everything required by LocationResult

COMMERCIAL PROVIDER

Investigate one realistic production provider using its official documentation/pricing/terms.

Do not recommend based only on blog posts or third-party comparisons.

ARCHITECTURE DECISION

After researching the providers, propose:

1. Primary provider
2. Optional fallback provider
3. Whether we should cache location resolutions
4. Suggested cache duration
5. Basic rate-limiting strategy
6. How API keys should be stored
7. How provider failures should be handled
8. How the provider response maps into LocationResult
9. Whether we need to change LocationResult before implementation

IMPORTANT

Do not introduce provider-specific fields into the frontend contract.

The architecture must remain:

Frontend
   ↓
/api/location/search
   ↓
LocationService
   ↓
GeocodingProvider
   ↓
Normalized LocationResult

Also consider that the user's onboarding currently accepts a free-form city/location string.

We are NOT implementing autocomplete yet.

REPORTING REQUIREMENT — MANDATORY

When finished, STOP and report:

1. Providers investigated
2. Official sources used
3. Provider-by-provider findings
4. Verified facts vs engineering assessment vs assumptions
5. Recommended primary provider
6. Recommended fallback provider, if any
7. Licensing/commercial considerations
8. Rate-limit considerations
9. API-key/security considerations
10. Caching recommendation
11. Failure-handling recommendation
12. Exact mapping into LocationResult
13. Whether LocationResult needs modification
14. Proposed implementation plan for the next step
15. Any unresolved questions

Do not write code.
Do not install anything.
Do not modify files.
STOP after the analysis report.