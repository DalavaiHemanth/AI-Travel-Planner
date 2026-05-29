"""country_card.py — Renders country information UI."""

import streamlit as st
from services.country import format_population, format_area


def render_country_card(info: dict):
    """Display a rich country information card."""
    # Header with flag and name
    col_flag, col_title = st.columns([1, 4])
    with col_flag:
        if info.get("flag_url"):
            st.image(info["flag_url"], width=120)
        else:
            st.markdown(f"<span style='font-size:80px'>{info.get('flag_emoji','🏳️')}</span>", unsafe_allow_html=True)
    with col_title:
        st.markdown(f"## {info['flag_emoji']} {info['name']}")
        st.caption(info.get("official_name", ""))
        st.markdown(f"🌍 **{info['region']}** · {info.get('subregion', '')}")
        if info.get("google_maps"):
            st.markdown(f"[📍 View on Google Maps]({info['google_maps']})")

    st.divider()

    # Key stats in metric columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🏛️ Capital", info["capital"])
    with col2:
        st.metric("👥 Population", format_population(info["population"]))
    with col3:
        area_str = format_area(info["area_km2"]) if info.get("area_km2") else "N/A"
        st.metric("📐 Area", area_str)
    with col4:
        tz = info["timezones"][0] if info.get("timezones") else "N/A"
        st.metric("🕐 Timezone", tz)

    st.divider()

    # Languages and currencies
    col_lang, col_curr = st.columns(2)
    with col_lang:
        st.markdown("**🗣️ Languages**")
        if info.get("languages"):
            for lang in info["languages"]:
                st.markdown(f"- {lang}")
        else:
            st.markdown("*Not available*")

    with col_curr:
        st.markdown("**💰 Currencies**")
        if info.get("currencies"):
            for curr in info["currencies"]:
                st.markdown(f"- **{curr['code']}** {curr['symbol']} — {curr['name']}")
        else:
            st.markdown("*Not available*")
