import React from 'react';
import {
  HeartPulse,
  Dumbbell,
  Plane,
  Users,
  Sprout,
  Car,
  Calendar,
  Waves,
  Check
} from 'lucide-react';

const ICON_MAP = {
  HeartPulse,
  Dumbbell,
  Plane,
  Users,
  Sprout,
  Car,
  Calendar,
  Waves
};

export default function InterestChip({ interest, isSelected, onToggle }) {
  const IconComponent = ICON_MAP[interest.iconName] || HeartPulse;

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      onToggle(interest.id);
    }
  };

  return (
    <div
      role="checkbox"
      aria-checked={isSelected}
      tabIndex={0}
      className={`interest-chip ${isSelected ? 'interest-chip--selected' : ''}`}
      onClick={() => onToggle(interest.id)}
      onKeyDown={handleKeyDown}
      id={`interest-chip-${interest.id}`}
    >
      <div className="interest-chip-header">
        <div className="interest-chip-icon">
          <IconComponent size={20} strokeWidth={2} />
        </div>
        <div className="interest-chip-checkbox">
          {isSelected && <Check size={12} strokeWidth={3} />}
        </div>
      </div>
      
      <div className="interest-chip-content">
        <span className="interest-chip-title">{interest.label}</span>
        <span className="interest-chip-desc">{interest.desc}</span>
      </div>
    </div>
  );
}
