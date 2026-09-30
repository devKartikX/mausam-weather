import React from 'react';
import { Droplets } from 'lucide-react';
import WeatherIcon from './WeatherIcon';

export default function HourlyForecast({ hourly = [] }) {
  if (!hourly || hourly.length === 0) return null;

  return (
    <section className="hourly-forecast-section">
      <div className="section-header-row">
        <h2 className="section-title">Hourly Forecast</h2>
        <span className="section-meta-text">Next 10 hours</span>
      </div>

      <div className="hourly-scroll-wrapper">
        <div className="hourly-scroll-container">
          {hourly.map((item, index) => {
            const isNow = index === 0;
            return (
              <div
                key={`${item.time}-${index}`}
                className={`hourly-card ${isNow ? 'hourly-card--current' : ''}`}
                id={`hourly-card-${index}`}
              >
                <span className="hourly-time">{item.time}</span>
                
                <div className="hourly-icon-wrap">
                  <WeatherIcon name={item.icon} size={22} strokeWidth={1.75} />
                </div>

                <span className="hourly-temp">{item.temp}°</span>

                <div className="hourly-pop">
                  {item.pop > 0 ? (
                    <>
                      <Droplets size={10} className="pop-icon" />
                      <span>{item.pop}%</span>
                    </>
                  ) : (
                    <span className="pop-empty">-</span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
