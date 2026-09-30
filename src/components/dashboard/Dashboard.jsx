import React, { useState, useEffect, useCallback } from 'react';
import {
  CloudSun,
  MapPin,
  SlidersHorizontal,
  ArrowLeft,
  Sparkles,
  Compass,
  AlertCircle,
  RefreshCw,
} from 'lucide-react';
import WeatherHero from './WeatherHero';
import WeatherMetrics from './WeatherMetrics';
import HourlyForecast from './HourlyForecast';
import DailyForecast from './DailyForecast';
import WeatherAlert from './WeatherAlert';
import PersonalizedInsightCard from '../personalized/PersonalizedInsightCard';
import { WeatherDashboardSkeleton } from '../common/Skeleton';
import { generatePersonalizedInsights } from '../../services/personalizationEngine';
import { INTERESTS } from '../../data/interests';
import { fetchWeatherForLocation } from '../../services/weatherClient';
import '../../styles/Dashboard.css';

/**
 * Dashboard — Step 25 update.
 *
 * userProfile now optionally includes:
 *   canonicalLocation: { city, state, country, latitude, longitude, timezone, displayName }
 *
 * Backward compatible: if canonicalLocation is missing, location string is used as before.
 */
export default function Dashboard({ userProfile, onEditPreferences }) {
  const { name, location, selectedInterests = [], canonicalLocation } = userProfile;

  // Resolve the weather query string — use city name for backend compatibility
  // canonicalLocation?.city is the authoritative value when available
  const weatherQuery = canonicalLocation?.city || location || '';

  // Friendly display text for header and loading message
  const displayLocation =
    canonicalLocation?.displayName || canonicalLocation?.city || location || '';

  const [weatherData, setWeatherData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState(null);
  const [retryNonce, setRetryNonce] = useState(0);

  const handleRetry = useCallback(() => {
    setRetryNonce((prev) => prev + 1);
  }, []);

  // Fetch weather data with cancellation to prevent race conditions during rapid city changes
  useEffect(() => {
    let isCancelled = false;

    if (!weatherQuery || !weatherQuery.trim()) {
      setIsLoading(false);
      setErrorMessage('No location specified. Please update your profile.');
      setWeatherData(null);
      return;
    }

    setIsLoading(true);
    setErrorMessage(null);
    setWeatherData(null);

    fetchWeatherForLocation(weatherQuery.trim())
      .then((data) => {
        if (!isCancelled) {
          setWeatherData(data);
          setIsLoading(false);
        }
      })
      .catch((err) => {
        if (!isCancelled) {
          setErrorMessage(err.message || 'Failed to load weather data.');
          setWeatherData(null);
          setIsLoading(false);
        }
      });

    return () => {
      isCancelled = true;
    };
  }, [weatherQuery, retryNonce]);

  // Generate deterministic personalized insights using real weather data
  const personalizedInsights = weatherData
    ? generatePersonalizedInsights(selectedInterests, weatherData)
    : [];

  // Format friendly interest names for contextual banner
  const activeInterestLabels = INTERESTS
    .filter((item) => selectedInterests.includes(item.id))
    .map((item) => item.label);

  const interestSummaryText = (() => {
    const count = activeInterestLabels.length;
    if (count === 0) return '';
    if (count === 1) return activeInterestLabels[0];
    if (count === 2) return `${activeInterestLabels[0]} & ${activeInterestLabels[1]}`;
    if (count === 3) return `${activeInterestLabels[0]}, ${activeInterestLabels[1]} & ${activeInterestLabels[2]}`;
    return `${activeInterestLabels[0]}, ${activeInterestLabels[1]} & ${count - 2} more`;
  })();

  // Use backend-resolved city name if available, else canonical city, else raw input
  const displayCity =
    weatherData?.location?.city ||
    canonicalLocation?.city ||
    location;

  return (
    <div className="dashboard-container">
      {/* 1. Header */}
      <header className="dashboard-header">
        <div className="header-brand-wrap">
          <CloudSun size={24} className="header-brand-icon" />
          <span className="header-brand-title">Mausam</span>
        </div>

        <div className="header-actions">
          <div className="header-location-pill" title={displayLocation || displayCity}>
            <MapPin size={13} className="header-location-icon" />
            <span>{displayCity}</span>
          </div>

          <button
            type="button"
            onClick={onEditPreferences}
            className="header-icon-btn"
            title="Edit Preferences"
            aria-label="Edit Preferences"
            id="header-edit-preferences-btn"
          >
            <SlidersHorizontal size={16} aria-hidden="true" />
          </button>
        </div>
      </header>

      {/* 2. Loading State */}
      {isLoading && (
        <WeatherDashboardSkeleton locationName={displayCity || weatherQuery} />
      )}

      {/* 3. Error State */}
      {!isLoading && errorMessage && (
        <div className="dashboard-state-container" role="alert">
          <div className="dashboard-error-icon-wrap">
            <AlertCircle size={28} />
          </div>
          <h3 className="dashboard-state-title">Weather Unavailable</h3>
          <p className="dashboard-state-desc">{errorMessage}</p>
          <button
            type="button"
            onClick={handleRetry}
            className="dashboard-retry-btn"
          >
            <RefreshCw size={14} />
            <span>Try Again</span>
          </button>
        </div>
      )}

      {/* 4. Loaded Dashboard Content */}
      {!isLoading && !errorMessage && weatherData && (
        <>
          {/* Weather Alert (displayed prominently near top if active) */}
          <WeatherAlert
            alerts={weatherData.alerts || []}
            alertsAvailable={weatherData.meta?.alertsAvailable !== false}
            alertsProvider={weatherData.meta?.alertsProvider || 'IMD / NDMA Sachet'}
          />

          {/* Personalized Greeting + Current Weather Hero */}
          <WeatherHero
            userName={name}
            userLocation={displayCity}
            weather={weatherData}
          />

          {/* =====================================================================
              PERSONALIZED INSIGHTS SECTION
              ===================================================================== */}
          <section className="personalized-section" id="personalized-section">
            <div className="section-header-row">
              <h2 className="section-title personalized-title">
                <Sparkles size={16} className="title-sparkle-icon" />
                <span>Personalized for you</span>
              </h2>
              {interestSummaryText && (
                <span className="personalized-badge">
                  {interestSummaryText}
                </span>
              )}
            </div>

            {personalizedInsights.length > 0 ? (
              <div className="personalized-cards-stack">
                {personalizedInsights.map((insight) => (
                  <PersonalizedInsightCard key={insight.id} insight={insight} />
                ))}
              </div>
            ) : (
              <div className="personalized-empty-card">
                <Compass size={24} className="empty-icon" />
                <p className="empty-text">
                  Select your interests to personalize your weather insights.
                </p>
                <button
                  type="button"
                  onClick={onEditPreferences}
                  className="empty-action-btn"
                >
                  Choose Interests
                </button>
              </div>
            )}
          </section>

          {/* General Atmospheric Conditions */}
          <WeatherMetrics current={weatherData.current} />

          {/* Hourly Forecast */}
          <HourlyForecast hourly={weatherData.hourly} />

          {/* 7-Day Forecast */}
          <DailyForecast daily={weatherData.daily} userLocation={displayCity} />
        </>
      )}

      {/* Footer / Profile Action */}
      <section className="dashboard-footer-action">
        <button
          type="button"
          onClick={onEditPreferences}
          className="footer-edit-btn"
          id="footer-edit-preferences-btn"
        >
          <ArrowLeft size={16} />
          <span>Edit Preferences</span>
        </button>
        <p className="footer-note">
          Switch interests or change city to update your profile.
        </p>
        <p className="footer-sources-note">
          Weather: Open-Meteo • AQI: US EPA • Warnings: Official IMD/NDMA CAP • Marine: Open-Meteo
        </p>
      </section>
    </div>
  );
}
