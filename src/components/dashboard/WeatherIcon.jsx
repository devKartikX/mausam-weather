import React from 'react';
import {
  Sun,
  CloudSun,
  Cloud,
  CloudRain,
  CloudLightning,
  CloudDrizzle
} from 'lucide-react';

const ICON_MAP = {
  Sun,
  CloudSun,
  Cloud,
  CloudRain,
  CloudLightning,
  CloudDrizzle
};

export default function WeatherIcon({ name, size = 24, className = '', strokeWidth = 2 }) {
  const Icon = ICON_MAP[name] || CloudSun;
  return <Icon size={size} className={className} strokeWidth={strokeWidth} />;
}
