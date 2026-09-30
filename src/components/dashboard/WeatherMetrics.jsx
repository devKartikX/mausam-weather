import React from 'react';
import {
  Droplets,
  Wind,
  CloudRain,
  Eye,
  Sun,
  Activity
} from 'lucide-react';

function getHumidityLabel(humidity) {
  if (humidity == null) return 'Unavailable';
  if (humidity < 30) return 'Dry';
  if (humidity <= 60) return 'Comfortable';
  return 'Humid';
}

function getRainLabel(prob) {
  if (prob == null) return 'Unavailable';
  if (prob < 20) return 'Low chance';
  if (prob < 50) return 'Moderate chance';
  return 'High chance';
}

function getVisibilityLabel(vis) {
  if (vis == null) return 'Unavailable';
  if (vis >= 7) return 'Good visibility';
  if (vis >= 4) return 'Moderate visibility';
  return 'Low visibility';
}

export default function WeatherMetrics({ current }) {
  if (!current) return null;

  const metrics = [
    {
      id: 'humidity',
      label: 'Humidity',
      value: current.humidity != null ? `${current.humidity}%` : 'Unavailable',
      sub: getHumidityLabel(current.humidity),
      icon: Droplets,
      color: '#38bdf8'
    },
    {
      id: 'wind',
      label: 'Wind',
      value: current.windSpeed != null ? `${current.windSpeed} km/h` : 'Unavailable',
      sub: current.windDirection ? `${current.windDirection} direction` : 'Calm',
      icon: Wind,
      color: '#818cf8'
    },
    {
      id: 'rain',
      label: 'Rain Chance',
      value: current.rainProbability != null ? `${current.rainProbability}%` : 'Unavailable',
      sub: getRainLabel(current.rainProbability),
      icon: CloudRain,
      color: '#60a5fa'
    },
    {
      id: 'visibility',
      label: 'Visibility',
      value: current.visibility != null ? `${current.visibility} km` : 'Unavailable',
      sub: getVisibilityLabel(current.visibility),
      icon: Eye,
      color: '#34d399'
    },
    {
      id: 'uv',
      label: 'UV Index',
      value: current.uvIndex != null ? current.uvIndex : 'Unavailable',
      sub: current.uvStatus || (current.uvIndex != null ? 'Normal' : 'Unavailable'),
      icon: Sun,
      color: '#fbbf24'
    },
    {
      id: 'aqi',
      label: 'Air Quality (US EPA)',
      value: current.aqi != null ? current.aqi : 'Unavailable',
      sub: current.aqi != null ? (current.aqiStatus || 'US EPA') : 'Not available',
      icon: Activity,
      color: '#f97316'
    }
  ];

  return (
    <section className="weather-metrics-section">
      <h2 className="section-title">Key Conditions</h2>
      <div className="metrics-grid">
        {metrics.map((metric) => {
          const Icon = metric.icon;
          return (
            <div key={metric.id} className="metric-tile" id={`metric-tile-${metric.id}`}>
              <div className="metric-tile-top">
                <div
                  className="metric-icon-wrap"
                  style={{ color: metric.color, backgroundColor: `${metric.color}18` }}
                >
                  <Icon size={18} strokeWidth={2} />
                </div>
                <span className="metric-label">{metric.label}</span>
              </div>
              <div className="metric-tile-bottom">
                <span className="metric-value">{metric.value}</span>
                <span className="metric-sub">{metric.sub}</span>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
