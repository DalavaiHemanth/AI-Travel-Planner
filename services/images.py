"""
images.py — Unsplash API wrapper with Picsum fallback.
Unsplash endpoint: https://api.unsplash.com/search/photos
"""

import requests
from config import get_secret

UNSPLASH_BASE = "https://api.unsplash.com"


def get_destination_images(query: str, count: int = 6) -> list[dict]:
    """
    Fetch destination images. Uses Unsplash if key is set, else Picsum fallback.
    """
    unsplash_key = get_secret("UNSPLASH_ACCESS_KEY")
    if unsplash_key and unsplash_key != "your_unsplash_access_key_here":
        try:
            return _fetch_unsplash(query, count, unsplash_key)
        except Exception:
            pass
    return _placeholder_images(query, count)


def _fetch_unsplash(query: str, count: int, access_key: str) -> list[dict]:
    url = f"{UNSPLASH_BASE}/search/photos"
    headers = {"Authorization": f"Client-ID {access_key}"}
    params = {"query": query, "per_page": min(count, 30), "orientation": "landscape"}
    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    images = []
    for item in data.get("results", [])[:count]:
        images.append({
            "url": item["urls"]["regular"],
            "thumb": item["urls"]["small"],
            "alt": item.get("alt_description") or f"{query} photo",
            "photographer": item["user"]["name"],
            "photographer_url": item["user"]["links"]["html"],
            "source_link": item["links"]["html"],
            "source": "Unsplash",
        })
    return images


def _placeholder_images(query: str, count: int) -> list[dict]:
    """Deterministic Picsum placeholders — always available, no auth needed."""
    seed_base = abs(hash(query)) % 1000
    images = []
    for i in range(count):
        seed = seed_base + i * 17
        images.append({
            "url": f"https://picsum.photos/seed/{seed}/800/500",
            "thumb": f"https://picsum.photos/seed/{seed}/400/250",
            "alt": f"{query} destination photo {i + 1}",
            "photographer": "Lorem Picsum",
            "photographer_url": "https://picsum.photos",
            "source_link": "https://picsum.photos",
            "source": "Picsum (demo — add UNSPLASH_ACCESS_KEY for real photos)",
        })
    return images
