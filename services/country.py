"""
country.py — REST Countries API wrapper.
Endpoint: https://restcountries.com/v3.1/name/{name}
No API key required.
"""

import requests

BASE_URL = "https://restcountries.com/v3.1"
FIELDS = "name,capital,population,languages,currencies,flags,latlng,region,subregion,timezones,area,maps"


def get_country_info(country_name: str) -> dict:
    """
    Fetch comprehensive country data from REST Countries API.

    Args:
        country_name: Country name (e.g., "Japan", "France")

    Returns:
        Parsed dict with country details, or raises on error.
    """
    url = f"{BASE_URL}/name/{country_name.strip()}"
    params = {"fields": FIELDS}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data or isinstance(data, dict) and data.get("status") == 404:
            raise ValueError(f"Country '{country_name}' not found.")

        # Pick the first exact / best match
        country = data[0]
        return _parse_country(country)

    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            raise ValueError(f"Country '{country_name}' not found. Please check the spelling.")
        raise RuntimeError(f"API error: {e}")
    except requests.exceptions.ConnectionError:
        raise RuntimeError("Could not connect to REST Countries API. Check your internet connection.")
    except requests.exceptions.Timeout:
        raise RuntimeError("Request timed out. Please try again.")


def _parse_country(raw: dict) -> dict:
    """Extract and clean fields from the raw API response."""

    # Currency info
    currencies_raw = raw.get("currencies", {})
    currencies = []
    for code, info in currencies_raw.items():
        currencies.append({
            "code": code,
            "name": info.get("name", code),
            "symbol": info.get("symbol", ""),
        })

    # Languages
    languages = list(raw.get("languages", {}).values())

    # Coordinates
    latlng = raw.get("latlng", [0, 0])
    lat = latlng[0] if len(latlng) > 0 else 0
    lon = latlng[1] if len(latlng) > 1 else 0

    # Capital
    capitals = raw.get("capital", [])
    capital = capitals[0] if capitals else "N/A"

    # Flags
    flags = raw.get("flags", {})
    flag_url = flags.get("svg") or flags.get("png") or ""
    flag_emoji = raw.get("flag", "")

    # Maps
    maps = raw.get("maps", {})
    google_maps = maps.get("googleMaps", "")

    return {
        "name": raw.get("name", {}).get("common", "Unknown"),
        "official_name": raw.get("name", {}).get("official", ""),
        "capital": capital,
        "population": raw.get("population", 0),
        "region": raw.get("region", ""),
        "subregion": raw.get("subregion", ""),
        "languages": languages,
        "currencies": currencies,
        "flag_url": flag_url,
        "flag_emoji": flag_emoji,
        "lat": lat,
        "lon": lon,
        "timezones": raw.get("timezones", []),
        "area_km2": raw.get("area", 0),
        "google_maps": google_maps,
    }


def format_population(pop: int) -> str:
    """Format population number with commas and B/M suffix."""
    if pop >= 1_000_000_000:
        return f"{pop / 1_000_000_000:.2f}B"
    elif pop >= 1_000_000:
        return f"{pop / 1_000_000:.2f}M"
    elif pop >= 1_000:
        return f"{pop:,}"
    return str(pop)


def format_area(area: float) -> str:
    """Format area in km²."""
    if area >= 1_000_000:
        return f"{area / 1_000_000:.2f}M km²"
    elif area >= 1_000:
        return f"{area:,.0f} km²"
    return f"{area:.0f} km²"
