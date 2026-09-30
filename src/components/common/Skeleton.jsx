import React from 'react';

/**
 * Skeleton Loader Component for Mausam
 * Provides accessible, lightweight placeholder loading blocks matching the design system tokens.
 */
export default function Skeleton({
  variant = 'text', // 'text' | 'rect' | 'circle' | 'pill'
  width,
  height,
  className = '',
  style = {},
  ...props
}) {
  const inlineStyles = {
    ...style,
    ...(width ? { width } : {}),
    ...(height ? { height } : {}),
  };

  return (
    <div
      className={`skeleton skeleton--${variant} ${className}`}
      style={inlineStyles}
      aria-hidden="true"
      {...props}
    />
  );
}

/**
 * WeatherDashboardSkeleton
 * Full-page structured skeleton that mirrors the Mausam Dashboard layout
 * without jarring layout shifts when data arrives.
 */
export function WeatherDashboardSkeleton({ locationName = 'your location' }) {
  return (
    <div className="dashboard-skeleton-view" aria-busy="true" aria-live="polite">
      {/* Header Loading Announcer */}
      <span className="sr-only">Loading latest weather information for {locationName}...</span>

      {/* Hero Skeleton */}
      <div className="skeleton-hero-card">
        <div className="skeleton-hero-top">
          <Skeleton variant="pill" width="130px" height="22px" />
          <Skeleton variant="pill" width="80px" height="20px" />
        </div>
        <div className="skeleton-hero-main">
          <div className="skeleton-hero-temp-col">
            <Skeleton variant="rect" width="110px" height="54px" style={{ borderRadius: '12px' }} />
            <Skeleton variant="text" width="140px" height="18px" style={{ marginTop: '8px' }} />
            <Skeleton variant="text" width="180px" height="14px" style={{ marginTop: '6px' }} />
          </div>
          <div className="skeleton-hero-icon-col">
            <Skeleton variant="circle" width="76px" height="76px" />
          </div>
        </div>
      </div>

      {/* Personalized Insights Skeleton */}
      <div className="skeleton-personalized-section">
        <div className="skeleton-section-header">
          <Skeleton variant="text" width="180px" height="18px" />
          <Skeleton variant="pill" width="100px" height="20px" />
        </div>
        <div className="skeleton-cards-stack">
          <div className="skeleton-insight-card">
            <div className="skeleton-card-header">
              <Skeleton variant="rect" width="140px" height="24px" style={{ borderRadius: '6px' }} />
              <Skeleton variant="pill" width="70px" height="20px" />
            </div>
            <Skeleton variant="text" width="85%" height="16px" style={{ marginTop: '10px' }} />
            <Skeleton variant="text" width="95%" height="14px" style={{ marginTop: '6px' }} />
            <div className="skeleton-metric-pills-row" style={{ display: 'flex', gap: '8px', marginTop: '12px' }}>
              <Skeleton variant="rect" width="90px" height="24px" style={{ borderRadius: '6px' }} />
              <Skeleton variant="rect" width="90px" height="24px" style={{ borderRadius: '6px' }} />
            </div>
          </div>
        </div>
      </div>

      {/* Metrics Grid Skeleton */}
      <div className="skeleton-metrics-section">
        <Skeleton variant="text" width="130px" height="16px" style={{ marginBottom: '12px' }} />
        <div className="metrics-grid">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="metric-tile metric-tile--skeleton">
              <div className="metric-tile-top">
                <Skeleton variant="circle" width="28px" height="28px" />
                <Skeleton variant="text" width="60px" height="12px" />
              </div>
              <div className="metric-tile-bottom" style={{ marginTop: '12px' }}>
                <Skeleton variant="text" width="45px" height="18px" />
                <Skeleton variant="text" width="70px" height="11px" style={{ marginTop: '4px' }} />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Hourly Forecast Skeleton */}
      <div className="skeleton-hourly-section">
        <div className="section-header-row" style={{ marginBottom: '12px' }}>
          <Skeleton variant="text" width="130px" height="16px" />
          <Skeleton variant="text" width="80px" height="12px" />
        </div>
        <div className="hourly-scroll-container">
          {[1, 2, 3, 4, 5, 6, 7].map((i) => (
            <div key={i} className="hourly-card hourly-card--skeleton">
              <Skeleton variant="text" width="32px" height="12px" />
              <Skeleton variant="circle" width="24px" height="24px" />
              <Skeleton variant="text" width="28px" height="15px" />
              <Skeleton variant="text" width="20px" height="10px" />
            </div>
          ))}
        </div>
      </div>

      {/* Daily Forecast Skeleton */}
      <div className="skeleton-daily-section">
        <Skeleton variant="text" width="120px" height="16px" style={{ marginBottom: '12px' }} />
        <div className="daily-list-card">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="daily-row" style={{ padding: '12px 0' }}>
              <Skeleton variant="text" width="45px" height="14px" />
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Skeleton variant="circle" width="20px" height="20px" />
                <Skeleton variant="text" width="70px" height="13px" />
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', justifyContent: 'flex-end' }}>
                <Skeleton variant="text" width="20px" height="12px" />
                <Skeleton variant="rect" width="60px" height="6px" style={{ borderRadius: '9999px' }} />
                <Skeleton variant="text" width="20px" height="12px" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
