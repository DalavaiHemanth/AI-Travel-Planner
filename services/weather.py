"""
weather.py — Open-Meteo API wrapper.
Endpoint: https://api.open-meteo.com/v1/forecast
No API key required.
"""

import requests
from datetime import datetime

BASE_URL = "https://api.open-meteo.com/v1/forecast"

# WMO Weather Interpretation Codes → (description, emoji)
WMO_CODES = {
    0:  ("Clear sky", "☀️"),
    1:  ("Mainly clear", "🌤️"),
    2:  ("Partly cloudy", "⛅"),
    3:  ("Overcast", "☁️"),
    45: ("Foggy", "🌫️"),
    48: ("Icy fog", "🌫️"),
    51: ("Light drizzle", "🌦️"),
    53: ("Drizzle", "🌦️"),
    55: ("Heavy drizzle", "🌧️"),
    61: ("Slight rain", "🌧️"),
    63: ("Moderate rain", "🌧️"),
    65: ("Heavy rain", "🌧️"),
    71: ("Slight snow", "🌨️"),
    73: ("Moderate snow", "❄️"),
    75: ("Heavy snow", "❄️"),
    77: ("Snow grains", "🌨️"),
    80: ("Rain showers", "🌦️"),
    81: ("Moderate showers", "🌧️"),
    82: ("Violent showers", "⛈️"),
    85: ("Snow showers", "🌨️"),
    86: ("Heavy snow showers", "❄️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm w/ hail", "⛈️"),
    99: ("Thunderstorm w/ heavy hail", "⛈️"),
}


def get_weather(lat: float, lon: float) -> dict:
    """
    Fetch current weather + 7-day forecast from Open-Meteo.

    Args:
        lat: Latitude
        lon: Longitude

    Returns:
        Dict with 'current' and 'forecast' keys.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,precipitation",
        "daily": "temperature_2m_max,temperature_2m_min,weather_code,precipitation_sum,wind_speed_10m_max",
        "timezone": "auto",
        "forecast_days": 7,
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return _parse_weather(data)

    except requests.exceptions.ConnectionError:
        raise RuntimeError("Could not connect to Open-Meteo API.")
    except requests.exceptions.Timeout:
        raise RuntimeError("Weather request timed out.")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Weather API error: {e}")


def _parse_weather(data: dict) -> dict:
    """Parse Open-Meteo response into a clean structure."""
    current_raw = data.get("current", {})
    daily_raw = data.get("daily", {})
    units = data.get("current_units", {})

    # Current conditions
    code = current_raw.get("weather_code", 0)
    desc, emoji = WMO_CODES.get(code, ("Unknown", "🌡️"))

    current = {
        "temperature": current_raw.get("temperature_2m", 0),
        "feels_like": current_raw.get("apparent_temperature", 0),
        "humidity": current_raw.get("relative_humidity_2m", 0),
        "wind_speed": current_raw.get("wind_speed_10m", 0),
        "precipitation": current_raw.get("precipitation", 0),
        "weather_code": code,
        "description": desc,
        "emoji": emoji,
        "temp_unit": units.get("temperature_2m", "°C"),
    }

    # 7-day forecast
    dates = daily_raw.get("time", [])
    max_temps = daily_raw.get("temperature_2m_max", [])
    min_temps = daily_raw.get("temperature_2m_min", [])
    weather_codes = daily_raw.get("weather_code", [])
    precip = daily_raw.get("precipitation_sum", [])
    wind = daily_raw.get("wind_speed_10m_max", [])

    forecast = []
    for i, date_str in enumerate(dates):
        day_code = weather_codes[i] if i < len(weather_codes) else 0
        day_desc, day_emoji = WMO_CODES.get(day_code, ("Unknown", "🌡️"))
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            day_label = dt.strftime("%a, %d %b")
        except ValueError:
            day_label = date_str

        forecast.append({
            "date": date_str,
            "day_label": day_label,
            "temp_max": max_temps[i] if i < len(max_temps) else 0,
            "temp_min": min_temps[i] if i < len(min_temps) else 0,
            "description": day_desc,
            "emoji": day_emoji,
            "precipitation": precip[i] if i < len(precip) else 0,
            "wind_speed": wind[i] if i < len(wind) else 0,
        })

    return {
        "current": current,
        "forecast": forecast,
        "timezone": data.get("timezone", "UTC"),
    }


def get_weather_advice(temp: float, code: int) -> str:
    """Return packing/clothing advice based on weather."""
    advice = []
    if temp < 5:
        advice.append("🧥 Heavy winter coat recommended")
    elif temp < 15:
        advice.append("🧣 Warm layers advised")
    elif temp < 25:
        advice.append("👕 Light jacket comfortable")
    else:
        advice.append("🩳 Light, breathable clothing ideal")

    if code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
        advice.append("☂️ Bring an umbrella")
    elif code in [71, 73, 75, 77, 85, 86]:
        advice.append("🥾 Waterproof boots needed")
    elif code == 0:
        advice.append("😎 Sunscreen recommended")

    return " · ".join(advice)
