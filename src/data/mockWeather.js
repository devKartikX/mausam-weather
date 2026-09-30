// Mock Weather Data for Jaipur, Rajasthan (Mausam Prototype)
export const mockWeatherData = {
  location: {
    city: 'Jaipur',
    state: 'Rajasthan',
    country: 'India',
    elevation: '431m',
    lastUpdated: 'Demo weather data'
  },
  current: {
    temp: 29,
    condition: 'Partly Cloudy',
    feelsLike: 31,
    highTemp: 33,
    lowTemp: 22,
    humidity: 46,
    windSpeed: 14,
    windDirection: 'NW',
    rainProbability: 15,
    visibility: 8,
    uvIndex: 6,
    uvStatus: 'High',
    aqi: 138,
    aqiStatus: 'Moderate',
    pm25: 48,
    pm10: 112,
    sunrise: '06:14 AM',
    sunset: '06:38 PM',
    icon: 'CloudSun',
    // Beach & Surf mock demo fields (not live/real marine data)
    waveHeight: 1.2,
    seaSurfaceTemp: 28,
    tidalInfo: {
      highTide: '10:45 AM',
      lowTide: '04:30 PM'
    }
  },
  hourly: [
    { time: 'Now', temp: 29, condition: 'Partly Cloudy', pop: 15, icon: 'CloudSun' },
    { time: '8 PM', temp: 27, condition: 'Clear', pop: 10, icon: 'Cloud' },
    { time: '9 PM', temp: 26, condition: 'Clear', pop: 5, icon: 'Cloud' },
    { time: '10 PM', temp: 25, condition: 'Clear', pop: 0, icon: 'Cloud' },
    { time: '11 PM', temp: 24, condition: 'Cool', pop: 0, icon: 'Cloud' },
    { time: '12 AM', temp: 23, condition: 'Cool', pop: 0, icon: 'Cloud' },
    { time: '6 AM', temp: 21, condition: 'Clear', pop: 0, icon: 'Sun' },
    { time: '7 AM', temp: 23, condition: 'Sunny', pop: 0, icon: 'Sun' },
    { time: '8 AM', temp: 26, condition: 'Sunny', pop: 5, icon: 'Sun' },
    { time: '9 AM', temp: 28, condition: 'Mostly Sunny', pop: 10, icon: 'CloudSun' }
  ],
  daily: [
    { day: 'Today', condition: 'Partly Cloudy', high: 33, low: 22, pop: 15, icon: 'CloudSun' },
    { day: 'Wed', condition: 'Sunny & Clear', high: 34, low: 23, pop: 10, icon: 'Sun' },
    { day: 'Thu', condition: 'Scattered Clouds', high: 32, low: 22, pop: 25, icon: 'CloudSun' },
    { day: 'Fri', condition: 'Passing Showers', high: 30, low: 21, pop: 60, icon: 'CloudRain' },
    { day: 'Sat', condition: 'Partly Cloudy', high: 31, low: 21, pop: 20, icon: 'CloudSun' },
    { day: 'Sun', condition: 'Mostly Sunny', high: 33, low: 22, pop: 10, icon: 'Sun' },
    { day: 'Mon', condition: 'Clear & Warm', high: 34, low: 23, pop: 5, icon: 'Sun' }
  ],
  alerts: [
    {
      id: 'alert-imd-01',
      level: 'advisory',
      badge: 'Simulated Advisory',
      title: 'Moderate UV Exposure & Afternoon Gusts',
      time: 'Demo Advisory • Peak hours',
      description: '[Simulated Advisory] UV Index reaching 6 (High) during peak hours with dry north-westerly wind gusts up to 22 km/h. Sensitive individuals should apply sunscreen and carry hydration.'
    }
  ]
};
