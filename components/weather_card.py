"""weather_card.py — Renders weather information UI."""

import streamlit as st
from services.weather import get_weather_advice


def render_weather_card(weather: dict):
    """Display current weather and 7-day forecast."""
    current = weather["current"]
    forecast = weather["forecast"]

    # Current conditions header
    st.markdown(
        f"""
        <div style="text-align:center; padding: 1.5rem 0;">
            <div style="font-size: 5rem; line-height:1">{current['emoji']}</div>
            <div style="font-size: 3.5rem; font-weight: 700; margin: 0.5rem 0;">
                {current['temperature']:.1f}{current['temp_unit']}
            </div>
            <div style="font-size: 1.2rem; color: #94a3b8;">{current['description']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🌡️ Feels Like", f"{current['feels_like']:.1f}°C")
    col2.metric("💧 Humidity", f"{current['humidity']}%")
    col3.metric("💨 Wind", f"{current['wind_speed']:.1f} km/h")
    col4.metric("🌧️ Precipitation", f"{current['precipitation']:.1f} mm")

    # Travel advice banner
    advice = get_weather_advice(current["temperature"], current["weather_code"])
    st.info(f"**Travel Tip:** {advice}")

    st.divider()
    st.markdown("### 📅 7-Day Forecast")

    # Forecast cards — 7 columns
    cols = st.columns(min(len(forecast), 7))
    for i, day in enumerate(forecast[:7]):
        with cols[i]:
            st.markdown(
                f"""
                <div style="text-align:center; padding:0.5rem; border-radius:8px;
                            background: rgba(255,255,255,0.05);">
                    <div style="font-size:0.75rem; color:#94a3b8; font-weight:600;">
                        {day['day_label'].split(',')[0]}
                    </div>
                    <div style="font-size:0.7rem; color:#64748b;">
                        {day['day_label'].split(',')[1].strip() if ',' in day['day_label'] else ''}
                    </div>
                    <div style="font-size:1.8rem; margin: 0.3rem 0;">{day['emoji']}</div>
                    <div style="font-size:0.85rem; font-weight:700;">{day['temp_max']:.0f}°</div>
                    <div style="font-size:0.75rem; color:#64748b;">{day['temp_min']:.0f}°</div>
                    <div style="font-size:0.65rem; color:#60a5fa; margin-top:0.2rem;">
                        {day['precipitation']:.1f}mm
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
