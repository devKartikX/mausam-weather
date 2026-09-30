"""
Location router — GET /api/location/search (Step 17, extended Step 24)

Step 17: Single-result canonical resolution (preserved for backward compat).
Step 24: Returns a JSON list of LocationResult objects for autocomplete.

The endpoint now always returns a list. A list of one item is the minimum
successful response for unambiguous queries. An empty list means no match.
"""

import logging
from typing import List

from fastapi import APIRouter, Query, HTTPException, status

from backend.schemas.location import LocationResult
from backend.services.location_service import location_service

logger = logging.getLogger(__name__)

router = APIRouter()

# Maximum autocomplete suggestions to return
_MAX_SUGGESTIONS = 8


@router.get(
    "/location/search",
    response_model=List[LocationResult],
    summary="Autocomplete / search locations",
    description=(
        "Returns up to 8 candidate LocationResult objects matching the given query string. "
        "Results are deduplicated by city+state+country. "
        "An empty list means no locations matched — this is not an error. "
        "Use the returned latitude/longitude/timezone for subsequent weather requests."
    ),
)
async def search_location(
    query: str = Query(
        ...,
        min_length=1,
        max_length=100,
        description="City or place name prefix to search",
        examples=["J", "Jai", "Jaipur", "London"],
    ),
):
    """
    Autocomplete location search — returns a JSON list of LocationResult objects.

    Rejects empty or whitespace-only queries with 400 Bad Request.
    Returns an empty list [] if no locations match (not 404).
    Returns 503 Service Unavailable if the provider fails AND the query has no offline fallback.
    """
    clean_query = query.strip()
    if not clean_query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Location query cannot be empty or whitespace only.",
        )

    try:
        results = await location_service.search_locations(clean_query, max_results=_MAX_SUGGESTIONS)
    except Exception as exc:
        logger.error("Location search failed for query '%s': %s", clean_query, exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Location search service temporarily unavailable. Please try again shortly.",
        )

    return results
