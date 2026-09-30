import React from 'react';
import {
  HeartPulse,
  Dumbbell,
  Plane,
  Car,
  Users,
  Sprout,
  Calendar,
  Waves,
  Lightbulb,
  CheckCircle2,
  AlertTriangle,
  Info
} from 'lucide-react';
import '../../styles/PersonalizedCard.css';

const ICON_MAP = {
  HeartPulse,
  Dumbbell,
  Plane,
  Car,
  Users,
  Sprout,
  Calendar,
  Waves
};

const STATUS_CONFIG = {
  favorable: {
    label: 'Favorable',
    badgeClass: 'status-badge--favorable',
    icon: CheckCircle2
  },
  moderate: {
    label: 'Moderate',
    badgeClass: 'status-badge--moderate',
    icon: Info
  },
  advisory: {
    label: 'Advisory',
    badgeClass: 'status-badge--advisory',
    icon: AlertTriangle
  }
};

export default function PersonalizedInsightCard({ insight }) {
  const {
    id,
    category,
    iconName,
    title,
    explanation,
    metrics = [],
    recommendation,
    status = 'favorable',
    accentColor
  } = insight;

  const CategoryIcon = ICON_MAP[iconName] || Info;
  const statusInfo = STATUS_CONFIG[status] || STATUS_CONFIG.favorable;
  const StatusIcon = statusInfo.icon;

  return (
    <article
      className={`personalized-insight-card personalized-insight-card--${status}`}
      style={{ '--card-accent': accentColor }}
      id={`personalized-card-${id}`}
    >
      {/* 1. Header: Category + Status Badge */}
      <div className="insight-card-header">
        <div className="insight-category-wrap">
          <div
            className="insight-category-icon"
            style={{ color: accentColor, backgroundColor: `${accentColor}18` }}
          >
            <CategoryIcon size={18} strokeWidth={2.2} />
          </div>
          <span className="insight-category-name">{category}</span>
        </div>

        <div className={`insight-status-badge ${statusInfo.badgeClass}`}>
          <StatusIcon size={12} strokeWidth={2.5} />
          <span>{statusInfo.label}</span>
        </div>
      </div>

      {/* 2. Main Title & Explanation */}
      <div className="insight-card-body">
        <h3 className="insight-title">{title}</h3>
        <p className="insight-explanation">{explanation}</p>
      </div>

      {/* 3. Metric Badges */}
      {metrics.length > 0 && (
        <div className="insight-metrics-grid">
          {metrics.map((metric, idx) => (
            <div key={idx} className={`insight-metric-pill insight-metric-pill--${metric.level}`}>
              <span className="metric-pill-label">{metric.label}</span>
              <span className="metric-pill-value">{metric.value}</span>
            </div>
          ))}
        </div>
      )}

      {/* 4. Actionable Recommendation */}
      {recommendation && (
        <div className="insight-recommendation-box">
          <div className="recommendation-icon-wrap">
            <Lightbulb size={15} className="recommendation-icon" />
          </div>
          <div className="recommendation-content">
            <span className="recommendation-prefix">Actionable Tip: </span>
            <span className="recommendation-text">{recommendation}</span>
          </div>
        </div>
      )}
    </article>
  );
}
