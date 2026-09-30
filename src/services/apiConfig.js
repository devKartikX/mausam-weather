/**
 * apiConfig.js — Centralized API Base URL configuration for Mausam.
 *
 * In development, VITE_API_BASE_URL can be omitted or empty, which defaults to '' (relative path)
 * and leverages Vite's dev server proxy to localhost:8000.
 *
 * In production (e.g. Render Static Site), VITE_API_BASE_URL is set to the deployed FastAPI HTTPS origin
 * (e.g. https://mausam-backend.onrender.com).
 */

const rawBaseUrl = import.meta.env.VITE_API_BASE_URL || '';

// Strip any trailing slash for consistent endpoint concatenation
export const API_BASE_URL = rawBaseUrl.endsWith('/')
  ? rawBaseUrl.slice(0, -1)
  : rawBaseUrl;
