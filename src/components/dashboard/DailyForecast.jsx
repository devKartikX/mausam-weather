import React from 'react';
import { Droplets, CalendarDays } from 'lucide-react';
import WeatherIcon from './WeatherIcon';

export default function DailyForecast({ daily = [], userLocation }) {
  if (!daily || daily.length === 0) return null;

  // Find global min and max across all days for proportional temperature bar
  const minTemp = Math.min(...daily.map((d) => d.low));
  const maxTemp = Math.max(...daily.map((d) => d.high));
  const tempSpan = maxTemp - minTemp || 1;

  return (
    <section className="daily-forecast-section">
      <div className="section-header-row">
        <h2 className="section-title">
          <CalendarDays size={16} className="title-icon" />
          <span>7-Day Outlook</span>
        </h2>
        <span className="section-meta-text">{userLocation || 'Local Area'}</span>
      </div>

      <div className="daily-list-card">
        {daily.map((item, index) => {
          // Calculate bar offsets
          const leftPercent = ((item.low - minTemp) / tempSpan) * 100;
          const widthPercent = Math.max(15, ((item.high - item.low) / tempSpan) * 100);

          return (
            <div key={item.day} className="daily-row" id={`daily-row-${index}`}>
              <span className={`daily-day-label ${item.day === 'Today' ? 'today-highlight' : ''}`}>
                {item.day}
              </span>

              <div className="daily-condition-col">
                <WeatherIcon name={item.icon} size={20} className="daily-icon" strokeWidth={1.75} />
                <span className="daily-condition-name">{item.condition}</span>
                {item.pop > 0 && (
                  <span className="daily-pop-pill">
                    <Droplets size={10} />
                    <span>{item.pop}%</span>
                  </span>
                )}
              </div>

              <div className="daily-temp-range">
                <span className="daily-low">{item.low}°</span>
                <div className="temp-bar-track">
                  <div
                    className="temp-bar-fill"
                    style={{
                      left: `${leftPercent}%`,
                      width: `${widthPercent}%`
                    }}
                  />
                </div>
                <span className="daily-high">{item.high}°</span>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
