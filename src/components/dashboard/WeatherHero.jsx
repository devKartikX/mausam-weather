import React from 'react';
import { MapPin, ArrowUp, ArrowDown } from 'lucide-react';
import WeatherIcon from './WeatherIcon';

export function getGreetingForHour(hour) {
  if (hour >= 0 && hour < 5) return 'Good night';
  if (hour >= 5 && hour < 12) return 'Good morning';
  if (hour >= 12 && hour < 17) return 'Good afternoon';
  if (hour >= 17 && hour < 21) return 'Good evening';
  return 'Good night';
}

export function getTimeGreeting(timeZone) {
  try {
    const formatter = new Intl.DateTimeFormat('en-US', {
      timeZone: timeZone || undefined,
      hour: 'numeric',
      hour12: false,
    });
    const parts = formatter.formatToParts(new Date());
    const hourPart = parts.find((p) => p.type === 'hour');
    let hour = parseInt(hourPart.value, 10);
    if (hour === 24) hour = 0;
    return getGreetingForHour(hour);
  } catch (e) {
    const hour = new Date().getHours();
    return getGreetingForHour(hour);
  }
}

function formatLastUpdated(lastUpdated, timeZone, isDemo) {
  if (isDemo) return 'Demo data';
  if (!lastUpdated) return 'Updated just now';
  try {
    // If it's an ISO timestamp or date string, format as HH:mm
    const date = new Date(lastUpdated);
    if (!isNaN(date.getTime())) {
      const timeStr = new Intl.DateTimeFormat('en-GB', {
        timeZone: timeZone || undefined,
        hour: '2-digit',
        minute: '2-digit',
        hour12: false,
      }).format(date);
      return `Updated ${timeStr}`;
    }
  } catch (_) {
    // fallback string extraction
  }
  if (typeof lastUpdated === 'string' && lastUpdated.includes('T')) {
    const timePart = lastUpdated.split('T')[1]?.slice(0, 5);
    if (timePart) return `Updated ${timePart}`;
  }
  return typeof lastUpdated === 'string' ? `Updated ${lastUpdated}` : 'Live';
}

export default function WeatherHero({ userName, userLocation, weather }) {
  if (!weather || !weather.current) return null;
  const { current, location, meta } = weather;
  const timeZone = location?.timezone;
  const greeting = getTimeGreeting(timeZone);
  const displayLocation = userLocation || location.city;
  const isDemo = Boolean(meta?.isDemo);

  return (
    <section className="weather-hero-section">
      {/* 2. Personalized Greeting Area */}
      <div className="dashboard-greeting">
        <h1 className="greeting-title">
          {greeting}, <span className="greeting-name">{userName || 'Friend'}</span> 👋
        </h1>
        <p className="greeting-subtitle">
          {isDemo ? (
            <>Simulated weather outlook for <span className="greeting-location">{displayLocation}</span></>
          ) : (
            <>Here's your weather outlook for <span className="greeting-location">{displayLocation}</span></>
          )}
        </p>
      </div>

      {/* 3. Hero Weather Card */}
      <div className="weather-hero-card">
        <div className="hero-top-row">
          <div className="hero-location-badge" title={displayLocation}>
            <MapPin size={14} className="hero-pin-icon" />
            <span>{displayLocation}</span>
          </div>
          <div className="hero-status-pills">
            {isDemo && (
              <span
                className="hero-demo-pill"
                title="Live provider temporarily rate-limited — showing simulated demo data"
              >
                Demo Data
              </span>
            )}
            {meta?.isStale && !isDemo && (
              <span className="hero-stale-pill" title="Showing recent data from cache">
                Showing recent data
              </span>
            )}
            <span className="hero-updated-time">{formatLastUpdated(location.lastUpdated, timeZone, isDemo)}</span>
          </div>
        </div>

        <div className="hero-main-content">
          <div className="hero-temp-block">
            <div className="hero-temp-display">
              <span className="hero-temp-value">{current.temp}</span>
              <span className="hero-temp-degree">°C</span>
            </div>
            <div className="hero-condition-text">{current.condition}</div>
            <div className="hero-temp-meta">
              <span>Feels like {current.feelsLike}°</span>
              <span className="meta-separator">•</span>
              <span className="high-low-tag">
                <ArrowUp size={12} className="temp-arrow high" /> {current.highTemp}°
                <ArrowDown size={12} className="temp-arrow low" /> {current.lowTemp}°
              </span>
            </div>
          </div>

          <div className="hero-icon-block">
            <div className="hero-icon-glow">
              <WeatherIcon name={current.icon} size={68} strokeWidth={1.5} className="hero-weather-icon" />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
