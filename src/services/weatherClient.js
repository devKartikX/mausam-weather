/**
 * Frontend Weather Client for Mausam (Step 20).
 *
 * Communicates with the FastAPI backend (/api/weather) to fetch normalized
 * weather data based on the user's location query.
 * Does NOT call external weather providers directly.
 */

import { API_BASE_URL } from './apiConfig';

export async function fetchWeatherForLocation(locationQuery) {
  if (!locationQuery || typeof locationQuery !== 'string' || !locationQuery.trim()) {
    throw new Error('A valid location query is required.');
  }

  const cleanQuery = locationQuery.trim();
  const encodedQuery = encodeURIComponent(cleanQuery);
  const endpoint = `${API_BASE_URL}/api/weather?location=${encodedQuery}`;

  let response;
  try {
    response = await fetch(endpoint, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    });
  } catch (networkError) {
    throw new Error(
      'Unable to connect to the weather service. Please check your connection and ensure the backend is running.'
    );
  }

  if (!response.ok) {
    let errorDetail = `Weather request failed (Status ${response.status})`;
    try {
      const errJson = await response.json();
      if (errJson && errJson.detail) {
        errorDetail = errJson.detail;
      }
    } catch (_) {
      // Keep default errorDetail if JSON parsing fails
    }
    throw new Error(errorDetail);
  }

  const data = await response.json();
  return data;
}
