"""
ai.py — Groq API wrapper for AI travel features.
Endpoint: https://api.groq.com/openai/v1/chat/completions
Requires GROQ_API_KEY in .env
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_BASE = "https://api.groq.com/openai/v1/chat/completions"
OPENROUTER_BASE = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "llama-3.3-70b-versatile"


def _call_llm(messages: list[dict], max_tokens: int = 2048) -> str:
    """
    Call Groq or OpenRouter LLM. Tries Groq first, falls back to OpenRouter.
    """
    groq_key = os.getenv("GROQ_API_KEY", "")
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "")

    if groq_key and groq_key != "your_groq_api_key_here":
        try:
            return _call_groq(messages, max_tokens, groq_key)
        except Exception as e:
            if not openrouter_key:
                raise RuntimeError(f"Groq API error: {e}")

    if openrouter_key and openrouter_key != "your_openrouter_api_key_here":
        return _call_openrouter(messages, max_tokens, openrouter_key)

    raise RuntimeError(
        "No AI API key configured. Please add GROQ_API_KEY to your .env file.\n"
        "Get a free key at: https://console.groq.com"
    )


def _call_groq(messages: list[dict], max_tokens: int, api_key: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": DEFAULT_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.7,
    }
    response = requests.post(GROQ_BASE, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def _call_openrouter(messages: list[dict], max_tokens: int, api_key: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://travel-planner.streamlit.app",
        "X-Title": "AI Travel Planner",
    }
    payload = {
        "model": "meta-llama/llama-3-8b-instruct:free",
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.7,
    }
    response = requests.post(OPENROUTER_BASE, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def generate_itinerary(
    destination: str,
    budget_inr: float,
    days: int,
    interests: list[str],
    currency_code: str = "USD",
) -> str:
    """Generate a detailed day-by-day travel itinerary."""
    interests_str = ", ".join(interests) if interests else "General sightseeing"
    system = (
        "You are an expert travel planner with deep knowledge of global destinations. "
        "Create detailed, practical, and inspiring travel itineraries. "
        "Always structure your response with clear Day headers. "
        "Include specific place names, realistic costs, and practical advice."
    )
    user = f"""Create a {days}-day travel itinerary for {destination}.

**Budget:** ₹{budget_inr:,.0f} INR total
**Interests:** {interests_str}
**Local Currency:** {currency_code}

Provide a complete itinerary with:

1. **Day-wise plan** (Day 1 through Day {days})
   - Morning activities with specific places/attractions
   - Afternoon activities with specific restaurants for lunch
   - Evening activities and dinner recommendations
   - Estimated cost per day in INR

2. **Budget Summary**
   - Daily average spend
   - Breakdown: accommodation / food / transport / activities
   - Assessment: Is ₹{budget_inr:,.0f} adequate, tight, or comfortable?

3. **Practical Tips**
   - Best time to visit
   - Local transport options
   - Cultural etiquette
   - Must-try local foods

Format as clean markdown with headers and bullet points."""

    return _call_llm(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=2500,
    )


def generate_packing_list(destination: str, days: int, weather_desc: str) -> str:
    """Generate a tailored packing list."""
    system = "You are a helpful travel assistant. Generate practical, concise packing lists."
    user = f"""Create a packing list for a {days}-day trip to {destination}.
Current weather: {weather_desc}

Organize into categories:
- 📄 Documents & Money
- 👕 Clothing (weather-appropriate)
- 🧴 Toiletries & Health
- 💊 Medications & First Aid
- 📱 Electronics & Gadgets
- 🎒 Miscellaneous

Keep each item brief. Mark essential items with ⭐."""

    return _call_llm(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=1000,
    )


def generate_local_tips(destination: str, interests: list[str]) -> str:
    """Generate local travel tips — phrases, safety, transport."""
    interests_str = ", ".join(interests) if interests else "general travel"
    system = "You are a local travel expert. Provide practical, insider knowledge."
    user = f"""Provide local travel tips for {destination} for a traveler interested in {interests_str}.

Include:
1. **Essential Phrases** — 8-10 useful local language phrases with pronunciation
2. **Safety Tips** — 5 important safety considerations
3. **Transport Guide** — How to get around (apps, passes, tips)
4. **Money & Tipping** — Local norms and payment culture
5. **Cultural Etiquette** — Do's and don'ts
6. **Hidden Gems** — 3-5 off-the-beaten-path recommendations

Keep it practical and specific to {destination}."""

    return _call_llm(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=1200,
    )


def analyze_budget(destination: str, budget_inr: float, days: int) -> str:
    """Analyze whether the budget is adequate for the trip."""
    system = "You are a travel budget expert. Give honest, data-driven budget assessments."
    user = f"""Analyze this travel budget:

**Destination:** {destination}
**Budget:** ₹{budget_inr:,.0f} INR
**Duration:** {days} days
**Daily budget:** ₹{budget_inr/days:,.0f} INR/day

Provide:
1. **Budget Assessment** — Is this budget: 💸 Too Tight / 💰 Moderate / 👑 Luxury?
2. **Cost Breakdown** — Typical costs for accommodation/food/transport/activities
3. **Money-Saving Tips** — 5 specific tips to stretch this budget
4. **Recommended Upgrades** — What you could add with 50% more budget
5. **Bottom Line** — Clear verdict and recommendation

Be specific with actual price ranges in INR."""

    return _call_llm(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=1000,
    )
