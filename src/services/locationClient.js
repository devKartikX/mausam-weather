/**
 * Frontend Location Search Client for Mausam (Step 25).
 *
 * Communicates ONLY with our FastAPI backend (/api/location/search).
 * Does NOT call Open-Meteo or any provider directly from React.
 *
 * Returns: Array of LocationResult objects (may be empty — not an error).
 * Throws:  Error on HTTP 4xx/5xx or network failure.
 */

import { API_BASE_URL } from './apiConfig';

/**
 * Search for locations matching the given query string.
 *
 * @param {string} query - User's typed text (min length 1)
 * @param {AbortSignal} [signal] - Optional AbortController signal for cancellation
 * @returns {Promise<Array<{city, state, country, latitude, longitude, timezone, displayName}>>}
 */
export async function searchLocations(query, signal) {
  if (!query || typeof query !== 'string') {
    throw new Error('A search query is required.');
  }

  const cleanQuery = query.trim();
  if (!cleanQuery) {
    throw new Error('Search query cannot be empty.');
  }

  const endpoint = `${API_BASE_URL}/api/location/search?query=${encodeURIComponent(cleanQuery)}`;

  let response;
  try {
    response = await fetch(endpoint, {
      method: 'GET',
      headers: { Accept: 'application/json' },
      signal,
    });
  } catch (networkError) {
    // AbortError is a normal cancellation, not a failure
    if (networkError && networkError.name === 'AbortError') {
      throw networkError;
    }
    throw new Error(
      'Unable to connect to the location service. Check your connection.'
    );
  }

  if (!response.ok) {
    // 422 = validation (too long / empty query)
    // 503 = provider down
    // 400 = whitespace-only query
    let detail = `Location search failed (HTTP ${response.status})`;
    try {
      const errJson = await response.json();
      if (errJson && errJson.detail) {
        detail = errJson.detail;
      }
    } catch (_) {
      // ignore JSON parse failure — keep default
    }
    throw new Error(detail);
  }

  const data = await response.json();
  // Backend guarantees an array; guard defensively
  return Array.isArray(data) ? data : [];
}
