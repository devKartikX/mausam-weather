"""
Base geocoding provider interface (Step 17, extended Step 24).

Defines the contract for geocoding providers. Any future provider (Nominatim, Geoapify, etc.)
must implement this minimal asynchronous interface.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from backend.schemas.location import LocationResult


class GeocodingProvider(ABC):
    """Abstract base class for geocoding providers."""

    @abstractmethod
    async def resolve(self, query: str) -> Optional[LocationResult]:
        """
        Resolve a user query into the single best-match canonical LocationResult.

        Used by the weather pipeline for exact city resolution.

        Returns:
            LocationResult if successfully geocoded.
            None if no matching locations were found (404).

        Raises:
            Exception / ProviderError on upstream failures or timeouts (triggering fallback/503).
        """
        pass

    @abstractmethod
    async def search(self, query: str, count: int = 8) -> List[LocationResult]:
        """
        Return up to `count` candidate LocationResult objects for autocomplete.

        Unlike resolve(), this method:
          - May return 0 results if the query matches nothing (not an error).
          - Returns results in provider relevance order.
          - Should NOT raise for empty results.

        Raises:
            Exception on upstream network failures or timeouts.
        """
        pass
