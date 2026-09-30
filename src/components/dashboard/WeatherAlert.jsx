import React from 'react';
import { AlertTriangle, Clock, ShieldCheck, ShieldAlert, Info } from 'lucide-react';

/**
 * WeatherAlert Component — Step 29 Polish
 * Handles:
 * 1. Active alerts (Advisory, Warning, Severe) with distinct visual severity, source attribution, and time
 * 2. Compact 'No active weather warnings' state when alertsAvailable === true && alerts.length === 0
 * 3. 'Official warning data unavailable' state when alertsAvailable === false
 */
export default function WeatherAlert({ alerts = [], alertsAvailable = true, alertsProvider = 'IMD / NDMA Sachet' }) {
  // Case 1: Official warning data unavailable (e.g. non-Indian location or upstream feed down)
  if (alertsAvailable === false) {
    return (
      <section className="weather-alerts-section" aria-label="Official Weather Warnings">
        <div className="weather-alert-compact-state weather-alert-compact--unavailable">
          <Info size={14} className="alert-compact-icon" aria-hidden="true" />
          <span className="alert-compact-text">Official warning data unavailable for this region</span>
          <span className="alert-compact-sub">({alertsProvider})</span>
        </div>
      </section>
    );
  }

  // Case 2: Alerts available but no active alerts for this location
  if (alertsAvailable === true && (!alerts || alerts.length === 0)) {
    return (
      <section className="weather-alerts-section" aria-label="Official Weather Warnings">
        <div className="weather-alert-compact-state weather-alert-compact--clear">
          <ShieldCheck size={14} className="alert-compact-icon" aria-hidden="true" />
          <span className="alert-compact-text">No active weather warnings</span>
          <span className="alert-compact-sub">Official IMD/NDMA CAP</span>
        </div>
      </section>
    );
  }

  // Case 3: Active weather alerts
  return (
    <section className="weather-alerts-section" aria-label="Official Weather Warnings">
      <div className="alerts-stack">
        {alerts.map((alert) => {
          // Normalize severity tier
          const levelLower = (alert.level || alert.badge || 'advisory').toLowerCase();
          const isSevere = levelLower.includes('severe') || levelLower.includes('danger') || levelLower.includes('red');
          const isWarning = levelLower.includes('warning') || levelLower.includes('orange');
          const severityClass = isSevere
            ? 'alert-card--severe'
            : isWarning
            ? 'alert-card--warning'
            : 'alert-card--advisory';

          const AlertIcon = isSevere ? ShieldAlert : AlertTriangle;

          return (
            <div
              key={alert.id}
              className={`weather-alert-card ${severityClass}`}
              id={`weather-alert-${alert.id}`}
              role="alert"
            >
              <div className="alert-card-top">
                <div className="alert-badge-wrap">
                  <AlertIcon size={14} className="alert-badge-icon" aria-hidden="true" />
                  <span className="alert-badge-text">{alert.badge || 'Advisory'}</span>
                </div>
                {alert.time && (
                  <div className="alert-time-wrap">
                    <Clock size={12} aria-hidden="true" />
                    <span>{alert.time}</span>
                  </div>
                )}
              </div>

              <h3 className="alert-title">{alert.title}</h3>
              <p className="alert-desc">{alert.description}</p>
              
              <div className="alert-source-footer">
                <span>Source: {alert.source || 'IMD / NDMA Sachet CAP Feed'}</span>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
