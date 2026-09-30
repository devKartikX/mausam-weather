/**
 * Deterministic Personalization Engine for Mausam Prototype
 * Generates targeted lifestyle insights based on user selected interests and current weather parameters.
 */

export function generatePersonalizedInsights(selectedInterests = [], weatherData) {
  if (!selectedInterests || selectedInterests.length === 0 || !weatherData) {
    return [];
  }

  const { current, alerts = [] } = weatherData;
  const insights = [];

  // 1. HEALTH & AIR QUALITY
  if (selectedInterests.includes('health')) {
    const isHighUV = current.uvIndex >= 6;
    const isModerateAQI = current.aqi > 100;

    insights.push({
      id: 'health',
      category: 'Health & Air Quality',
      iconName: 'HeartPulse',
      title: 'Respiratory & UV Exposure Advisory',
      explanation: `AQI is currently ${current.aqi} (${current.aqiStatus}) and UV index is ${current.uvIndex} (${current.uvStatus}).`,
      metrics: [
        {
          label: 'Air Quality',
          value: `${current.aqi} (${current.aqiStatus})`,
          level: isModerateAQI ? 'warning' : 'good'
        },
        {
          label: 'UV Index',
          value: `${current.uvIndex} (${current.uvStatus})`,
          level: isHighUV ? 'warning' : 'good'
        },
        {
          label: 'Humidity',
          value: `${current.humidity}%`,
          level: 'normal'
        }
      ],
      recommendation: isModerateAQI || isHighUV
        ? 'Limit prolonged outdoor exertion during peak afternoon hours (12:00 PM – 3:30 PM). Use SPF 30+ sunscreen and stay hydrated.'
        : 'Outdoor air quality and UV levels are within comfortable safety thresholds today.',
      status: isModerateAQI || isHighUV ? 'advisory' : 'favorable',
      accentColor: '#ec4899'
    });
  }

  // 2. FITNESS & OUTDOOR WORKOUTS
  if (selectedInterests.includes('fitness')) {
    const isHot = current.temp >= 30;
    const isWindy = current.windSpeed > 20;

    insights.push({
      id: 'fitness',
      category: 'Fitness & Workouts',
      iconName: 'Dumbbell',
      title: 'Outdoor Workout & Running Assessment',
      explanation: `Current temperature is ${current.temp}°C (feels like ${current.feelsLike}°C) with ${current.windSpeed} km/h wind and low rain probability (${current.rainProbability}%).`,
      metrics: [
        {
          label: 'Training Score',
          value: isHot ? 'Moderate Heat' : 'Ideal Training',
          level: isHot ? 'warning' : 'good'
        },
        {
          label: 'Optimal Window',
          value: '6:00 AM – 8:30 AM',
          level: 'good'
        },
        {
          label: 'Evening Run',
          value: 'After 6:30 PM',
          level: 'good'
        }
      ],
      recommendation: isHot
        ? 'Morning and late evening offer optimal conditions for outdoor running. Avoid high-intensity cardio under peak midday sun.'
        : 'Great weather for outdoor workouts, running, or cycling. Stay adequately hydrated.',
      status: 'favorable',
      accentColor: '#10b981'
    });
  }

  // 3. TRAVEL & TRIPS
  if (selectedInterests.includes('travel')) {
    const hasActiveAlert = alerts.length > 0;
    const isGoodVisibility = current.visibility >= 6;

    insights.push({
      id: 'travel',
      category: 'Travel & Trips',
      iconName: 'Plane',
      title: 'Regional Travel & Packing Outlook',
      explanation: `Visibility is clear at ${current.visibility} km with only ${current.rainProbability}% rain chance and ${current.condition.toLowerCase()} skies.`,
      metrics: [
        {
          label: 'Road Visibility',
          value: `${current.visibility} km (Clear)`,
          level: isGoodVisibility ? 'good' : 'warning'
        },
        {
          label: 'Rain Risk',
          value: `${current.rainProbability}% (Low)`,
          level: 'good'
        },
        {
          label: 'Advisories',
          value: hasActiveAlert ? 'Afternoon Gusts' : 'None',
          level: hasActiveAlert ? 'warning' : 'good'
        }
      ],
      recommendation: hasActiveAlert
        ? 'Travel conditions are favorable across highways. Keep sunglasses handy and be cautious of occasional dry crosswinds on open roads.'
        : 'Excellent conditions for inter-city travel and sightseeing.',
      status: hasActiveAlert ? 'moderate' : 'favorable',
      accentColor: '#6366f1'
    });
  }

  // 4. COMMUTING & TRANSIT
  if (selectedInterests.includes('commuting')) {
    const isLowRain = current.rainProbability < 25;
    const isClearRoads = current.visibility >= 5;

    insights.push({
      id: 'commuting',
      category: 'Daily Commute',
      iconName: 'Car',
      title: 'Rush-Hour Transit Conditions',
      explanation: `Clear commute visibility (${current.visibility} km) with dry road surfaces and negligible rain impact.`,
      metrics: [
        {
          label: 'Road Conditions',
          value: isLowRain ? 'Dry & Clear' : 'Wet Roads',
          level: isLowRain ? 'good' : 'warning'
        },
        {
          label: 'Visibility',
          value: `${current.visibility} km`,
          level: isClearRoads ? 'good' : 'warning'
        },
        {
          label: 'Wind Factor',
          value: `${current.windSpeed} km/h ${current.windDirection}`,
          level: 'normal'
        }
      ],
      recommendation: isClearRoads && isLowRain
        ? 'Smooth commute expected for evening rush hour. No rain delays anticipated on major transit routes.'
        : 'Allow extra transit time due to weather-related visibility or road condition slowdowns.',
      status: 'favorable',
      accentColor: '#f59e0b'
    });
  }

  // 5. FAMILY & OUTDOOR SAFETY
  if (selectedInterests.includes('family')) {
    const isHighUV = current.uvIndex >= 6;
    const isHighAQI = current.aqi > 100;
    const isRainy = current.rainProbability >= 40;
    const hasAlert = alerts.length > 0;

    insights.push({
      id: 'family',
      category: 'Family & Outdoor Safety',
      iconName: 'Users',
      title: 'Family Outdoor Conditions',
      explanation: `UV index is ${current.uvIndex} (${current.uvStatus}), AQI is ${current.aqi} (${current.aqiStatus}), and rain chance is ${current.rainProbability}%. Temperature feels like ${current.feelsLike}°C.`,
      metrics: [
        {
          label: 'UV Index',
          value: `${current.uvIndex} — ${current.uvStatus}`,
          level: isHighUV ? 'warning' : 'good'
        },
        {
          label: 'Air Quality',
          value: `${current.aqi} (${current.aqiStatus})`,
          level: isHighAQI ? 'warning' : 'good'
        },
        {
          label: 'Rain Chance',
          value: `${current.rainProbability}%`,
          level: isRainy ? 'warning' : 'good'
        }
      ],
      recommendation: isHighUV && isHighAQI
        ? 'Consider applying sunscreen before outdoor activity and limiting prolonged exposure during peak afternoon hours. It may help to keep windows closed if children have respiratory sensitivities.'
        : isHighUV
        ? 'Consider applying sunscreen and seeking shade between 11 AM – 3 PM. Rain is unlikely, so conditions may be favorable for outdoor play.'
        : isRainy
        ? 'It may be useful to carry rain gear for school pickup and outdoor plans. Conditions otherwise comfortable.'
        : hasAlert
        ? 'Consider checking the active weather advisory before extended outdoor activities.'
        : 'Outdoor conditions appear comfortable. Applying a light sunscreen may be useful given moderate UV levels.',
      status: isHighUV || isHighAQI ? 'advisory' : 'favorable',
      accentColor: '#f97316'
    });
  }

  // 6. AGRICULTURE & GARDEN
  if (selectedInterests.includes('agriculture')) {
    const isGoodSprayWindow = current.windSpeed <= 15;
    const isHighRainChance = current.rainProbability >= 50;
    const isModerateRainChance = current.rainProbability >= 25 && current.rainProbability < 50;
    const isHighHumidity = current.humidity >= 70;

    // Look ahead: any day in the 7-day forecast with high rain probability?
    const rainyDaysAhead = weatherData.daily
      ? weatherData.daily.filter((d) => d.pop >= 50).length
      : 0;

    insights.push({
      id: 'agriculture',
      category: 'Farm & Garden',
      iconName: 'Sprout',
      title: 'Farm & Garden Conditions',
      explanation: `Humidity is ${current.humidity}%, wind is ${current.windSpeed} km/h, and rain probability is ${current.rainProbability}% today. ${rainyDaysAhead > 0 ? `${rainyDaysAhead} day(s) with ≥50% rain chance in the next 7 days.` : 'No heavy rain expected this week.'}`,
      metrics: [
        {
          label: 'Rain Today',
          value: `${current.rainProbability}% chance`,
          level: isHighRainChance ? 'warning' : isModerateRainChance ? 'normal' : 'good'
        },
        {
          label: 'Humidity',
          value: `${current.humidity}%`,
          level: isHighHumidity ? 'warning' : 'normal'
        },
        {
          label: 'Spray Window',
          value: isGoodSprayWindow ? 'Suitable' : 'Avoid (Windy)',
          level: isGoodSprayWindow ? 'good' : 'warning'
        }
      ],
      recommendation: isHighRainChance
        ? 'Rain likely today — consider delaying irrigation and any chemical spraying. Monitor fields for waterlogging.'
        : isModerateRainChance
        ? 'Moderate rain chance. Irrigation may not be needed, and it may be prudent to delay spraying if wind picks up.'
        : isGoodSprayWindow
        ? `Low rain chance and calm wind (${current.windSpeed} km/h) — conditions may be suitable for fertilizer or pesticide application; verify with local guidance.`
        : `Wind at ${current.windSpeed} km/h — consider avoiding spraying today to reduce chemical drift risk, and plan for calmer conditions.`,
      status: isHighRainChance || !isGoodSprayWindow ? 'advisory' : 'favorable',
      accentColor: '#22c55e'
    });
  }

  // 7. OUTDOOR EVENTS
  if (selectedInterests.includes('events')) {
    const isComfortable = current.feelsLike <= 32 && current.humidity < 65;
    const isHighRain = current.rainProbability >= 40;
    const isWindy = current.windSpeed > 20;
    const isHighUV = current.uvIndex >= 6;
    const hasAlert = alerts.length > 0;

    let overallStatus = 'favorable';
    if (isHighRain || isWindy) overallStatus = 'advisory';
    else if (hasAlert || isHighUV) overallStatus = 'moderate';

    insights.push({
      id: 'events',
      category: 'Outdoor Events',
      iconName: 'Calendar',
      title: 'Outdoor Event Conditions',
      explanation: `Temperature ${current.temp}°C (feels ${current.feelsLike}°C), ${current.condition.toLowerCase()}. Wind at ${current.windSpeed} km/h with ${current.rainProbability}% rain probability.`,
      metrics: [
        {
          label: 'Feels Like',
          value: `${current.feelsLike}°C`,
          level: isComfortable ? 'good' : 'warning'
        },
        {
          label: 'Rain Risk',
          value: `${current.rainProbability}%`,
          level: isHighRain ? 'warning' : 'good'
        },
        {
          label: 'Wind',
          value: `${current.windSpeed} km/h`,
          level: isWindy ? 'warning' : 'good'
        },
        {
          label: 'UV',
          value: `${current.uvIndex} (${current.uvStatus})`,
          level: isHighUV ? 'warning' : 'good'
        }
      ],
      recommendation: isHighRain
        ? 'Significant rain chance — consider indoor backup options or waterproofing arrangements for outdoor setups.'
        : isWindy
        ? 'Winds may affect open structures and decorations. Secure temporary setups and monitor gusts.'
        : isHighUV && isComfortable
        ? 'Outdoor conditions are generally favorable. Provide shade and sun protection during peak afternoon UV hours.'
        : hasAlert
        ? 'Check the active IMD advisory before finalizing outdoor arrangements.'
        : 'Good conditions for outdoor events. Low rain risk and comfortable temperatures.',
      status: overallStatus,
      accentColor: '#a855f7'
    });
  }

  // 8. BEACH & SURF
  if (selectedInterests.includes('beach-surf')) {
    const { waveHeight, waveDirection, wavePeriod } = current;
    const isHighUV = current.uvIndex >= 6;
    const isWindy = current.windSpeed > 20;
    const isRainy = current.rainProbability >= 30;

    if (waveHeight != null) {
      // Coastal location with real marine data
      const surfCondition = waveHeight <= 1.0
        ? 'Calm — beginner friendly'
        : waveHeight <= 2.0
        ? 'Moderate — intermediate conditions'
        : 'Rough — experienced surfers only';

      insights.push({
        id: 'beach-surf',
        category: 'Beach & Surf',
        iconName: 'Waves',
        title: 'Coastal & Surf Conditions',
        explanation: `Live marine telemetry: wave height ~${waveHeight}m${wavePeriod ? `, period ${wavePeriod}s` : ''}, wind ${current.windSpeed} km/h ${current.windDirection}.`,
        metrics: [
          {
            label: 'Wave Height',
            value: `${waveHeight}m (Open-Meteo Marine)`,
            level: waveHeight > 2.0 ? 'warning' : 'good'
          },
          ...(wavePeriod != null ? [{
            label: 'Wave Period',
            value: `${wavePeriod}s`,
            level: 'good'
          }] : []),
          {
            label: 'UV Index',
            value: `${current.uvIndex} (${current.uvStatus})`,
            level: isHighUV ? 'warning' : 'good'
          },
          {
            label: 'Wind',
            value: `${current.windSpeed} km/h ${current.windDirection}`,
            level: isWindy ? 'warning' : 'good'
          }
        ],
        recommendation: isRainy
          ? 'Precipitation expected along the coast. Watch for choppy surf and reduced beach comfort.'
          : isWindy
          ? `Strong winds may create choppy surf. ${surfCondition}. Apply SPF 50+ sunscreen.`
          : `Marine conditions are favorable for beach activities. ${surfCondition}. Apply sunscreen — UV is ${current.uvStatus}.`,
        status: isWindy || isRainy ? 'advisory' : 'favorable',
        accentColor: '#0ea5e9'
      });
    } else {
      // Inland location where marine/surf telemetry is not applicable
      insights.push({
        id: 'beach-surf',
        category: 'Beach & Surf',
        iconName: 'Waves',
        title: 'Marine Conditions',
        explanation: 'Marine and surf telemetry is not applicable for this inland location. Open-Meteo Marine operates along coastal coordinates.',
        metrics: [
          {
            label: 'Wave Height',
            value: 'N/A (Inland)',
            level: 'normal'
          },
          {
            label: 'Wind',
            value: `${current.windSpeed} km/h ${current.windDirection}`,
            level: isWindy ? 'warning' : 'good'
          }
        ],
        recommendation: 'Beach and surf telemetry requires a coastal location. Switch location to a coastal city like Mumbai or Chennai to view active marine conditions.',
        status: 'moderate',
        accentColor: '#0ea5e9'
      });
    }
  }

  return insights;
}
