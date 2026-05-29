"""
currency.py — Open Exchange Rate API wrapper.
Endpoint: https://open.er-api.com/v6/latest/{base}
No API key required for free tier.
"""

import requests
from datetime import datetime

BASE_URL = "https://open.er-api.com/v6/latest"

# Common currency symbols for display
CURRENCY_SYMBOLS = {
    "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥", "INR": "₹",
    "CNY": "¥", "KRW": "₩", "AUD": "A$", "CAD": "C$", "CHF": "Fr",
    "SGD": "S$", "THB": "฿", "MYR": "RM", "IDR": "Rp", "PHP": "₱",
    "VND": "₫", "BDT": "৳", "PKR": "₨", "LKR": "Rs", "NPR": "Rs",
    "AED": "د.إ", "SAR": "﷼", "QAR": "﷼", "TRY": "₺", "BRL": "R$",
    "MXN": "$", "ZAR": "R", "EGP": "£", "NGN": "₦", "KES": "KSh",
}

# Popular travel currencies to show by default
POPULAR_CURRENCIES = [
    "USD", "EUR", "GBP", "JPY", "AUD", "CAD", "SGD", "THB",
    "AED", "CHF", "KRW", "MYR", "IDR", "VND", "TRY", "BRL",
]


def get_exchange_rates(base_currency: str = "INR") -> dict:
    """
    Fetch all exchange rates with the given base currency.

    Args:
        base_currency: ISO 4217 code (e.g., "INR", "USD")

    Returns:
        Dict with rates, timestamp, base currency.
    """
    url = f"{BASE_URL}/{base_currency.upper()}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("result") != "success":
            raise RuntimeError(f"Exchange rate API returned error: {data.get('error-type', 'unknown')}")

        return _parse_rates(data)

    except requests.exceptions.ConnectionError:
        raise RuntimeError("Could not connect to Exchange Rate API.")
    except requests.exceptions.Timeout:
        raise RuntimeError("Currency request timed out.")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Currency API error: {e}")


def _parse_rates(data: dict) -> dict:
    """Parse exchange rate API response."""
    timestamp_unix = data.get("time_last_update_unix", 0)
    try:
        updated_str = datetime.utcfromtimestamp(timestamp_unix).strftime("%d %b %Y, %H:%M UTC")
    except Exception:
        updated_str = data.get("time_last_update_utc", "Unknown")

    return {
        "base": data.get("base_code", "INR"),
        "rates": data.get("rates", {}),
        "last_updated": updated_str,
        "next_update": data.get("time_next_update_utc", ""),
    }


def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """
    Convert an amount from one currency to another.

    Args:
        amount: Amount to convert
        from_currency: Source ISO currency code
        to_currency: Target ISO currency code

    Returns:
        Dict with converted amount, rate, formatted strings.
    """
    rates_data = get_exchange_rates(from_currency)
    rates = rates_data["rates"]

    if to_currency.upper() not in rates:
        raise ValueError(f"Currency '{to_currency}' not found.")

    rate = rates[to_currency.upper()]
    converted = amount * rate

    from_sym = CURRENCY_SYMBOLS.get(from_currency.upper(), from_currency)
    to_sym = CURRENCY_SYMBOLS.get(to_currency.upper(), to_currency)

    return {
        "from_currency": from_currency.upper(),
        "to_currency": to_currency.upper(),
        "from_symbol": from_sym,
        "to_symbol": to_sym,
        "amount": amount,
        "converted": converted,
        "rate": rate,
        "last_updated": rates_data["last_updated"],
        "formatted_from": f"{from_sym}{amount:,.2f}",
        "formatted_to": f"{to_sym}{converted:,.2f}",
    }


def get_popular_conversions(amount: float, from_currency: str = "INR") -> list[dict]:
    """
    Convert an amount to all popular travel currencies at once.

    Args:
        amount: Amount in from_currency
        from_currency: Base currency code

    Returns:
        List of conversion dicts sorted by currency code.
    """
    rates_data = get_exchange_rates(from_currency)
    rates = rates_data["rates"]

    results = []
    for code in POPULAR_CURRENCIES:
        if code == from_currency.upper():
            continue
        if code not in rates:
            continue
        rate = rates[code]
        converted = amount * rate
        sym = CURRENCY_SYMBOLS.get(code, code)
        results.append({
            "currency": code,
            "symbol": sym,
            "rate": rate,
            "converted": converted,
            "formatted": f"{sym}{converted:,.2f}",
        })

    return results


def get_currency_symbol(code: str) -> str:
    """Return the symbol for a currency code."""
    return CURRENCY_SYMBOLS.get(code.upper(), code)
