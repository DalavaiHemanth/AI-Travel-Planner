"""
app.py — AI Travel Planner
Main Streamlit application entry point.

Run with:
    streamlit run app.py
"""

import os
import streamlit as st
from dotenv import load_dotenv
from config import get_secret

# Load environment variables
load_dotenv()

# ── Page Config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="AI Travel Planner ✈️",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/your-repo/travel-planner",
        "Report a bug": "https://github.com/your-repo/travel-planner/issues",
        "About": "# AI Travel Planner\nBuilt with Streamlit + Groq + REST APIs",
    },
)

# ── Load Custom CSS ─────────────────────────────────────────────────────────
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Import Services ─────────────────────────────────────────────────────────
from services.country import get_country_info
from services.weather import get_weather
from services.currency import convert_currency
from services.images import get_destination_images
from services.ai import generate_itinerary, generate_packing_list, generate_local_tips, analyze_budget

# ── Import Components ───────────────────────────────────────────────────────
from components.country_card import render_country_card
from components.weather_card import render_weather_card
from components.currency_card import render_currency_card
from components.image_gallery import render_image_gallery
from components.itinerary_display import (
    render_itinerary,
    render_packing_list,
    render_local_tips,
    render_budget_analysis,
)

# ── Session State Init ───────────────────────────────────────────────────────
for key in ["country_data", "weather_data", "images_data", "searched_destination", "destination_input"]:
    if key not in st.session_state:
        st.session_state[key] = "Japan" if key == "destination_input" else None

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div class="sidebar-logo">✈️ TravelAI</div>',
        unsafe_allow_html=True,
    )
    st.caption("Your AI-powered travel companion")
    st.divider()

    st.markdown("### 🌍 Trip Details")

    destination = st.text_input(
        "Destination",
        placeholder="e.g. Japan, France, Thailand",
        help="Enter any country or city name",
        key="destination_input",
    )

    budget_inr = st.number_input(
        "Budget (INR ₹)",
        min_value=1000.0,
        max_value=10_000_000.0,
        value=50000.0,
        step=5000.0,
        format="%.0f",
        help="Total trip budget in Indian Rupees",
        key="budget_input",
    )

    days = st.slider(
        "Number of Days",
        min_value=1,
        max_value=30,
        value=5,
        key="days_input",
        help="Duration of your trip",
    )

    interests = st.multiselect(
        "Interests",
        options=[
            "🍜 Food & Cuisine", "🎌 Anime & Pop Culture", "🏛️ History & Culture",
            "🌿 Nature & Hiking", "🎨 Art & Museums", "🛍️ Shopping",
            "🏖️ Beach & Relaxation", "🎭 Nightlife", "📸 Photography",
            "⛩️ Temples & Religion", "🎵 Music & Festivals", "🏔️ Adventure Sports",
        ],
        default=["🍜 Food & Cuisine", "🎌 Anime & Pop Culture"],
        key="interests_input",
    )

    st.divider()

    search_btn = st.button(
        "🔍 Plan My Trip",
        use_container_width=True,
        type="primary",
    )

    # API key status indicators
    st.divider()
    st.markdown("### 🔑 API Status")

    groq_key = get_secret("GROQ_API_KEY")
    unsplash_key = get_secret("UNSPLASH_ACCESS_KEY")

    groq_ok = groq_key and groq_key != "your_groq_api_key_here"
    unsplash_ok = unsplash_key and unsplash_key != "your_unsplash_access_key_here"

    st.markdown(
        f"{'✅' if groq_ok else '⚠️'} Groq AI — {'Connected' if groq_ok else '[Add key to .env](https://console.groq.com)'}"
    )
    st.markdown(
        f"{'✅' if unsplash_ok else '⚠️'} Unsplash — {'Connected' if unsplash_ok else 'Using Picsum fallback'}"
    )
    st.markdown("✅ REST Countries — Free")
    st.markdown("✅ Open-Meteo — Free")
    st.markdown("✅ Exchange Rate — Free")


# ── Hero Banner ──────────────────────────────────────────────────────────────
if not st.session_state.searched_destination:
    st.markdown(
        """
        <div class="hero-banner">
            <h1 style="font-size:2.5rem; font-weight:800; margin:0;
                       background: linear-gradient(135deg, #60a5fa, #a78bfa, #34d399);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       background-clip: text;">
                ✈️ AI Travel Planner
            </h1>
            <p style="color:#94a3b8; font-size:1.1rem; margin: 0.5rem 0 0 0;">
                Discover destinations, plan itineraries, and explore the world — powered by AI.
            </p>
            <div style="margin-top:1rem; display:flex; gap:1rem; flex-wrap:wrap;">
                <span class="status-badge">🌍 Country Info</span>
                <span class="status-badge">🌤️ Live Weather</span>
                <span class="status-badge">💱 Currency Rates</span>
                <span class="status-badge">📸 Destination Photos</span>
                <span class="status-badge">🤖 AI Itinerary</span>
                <span class="status-badge">🎒 Packing Lists</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info("👈 Enter a destination in the sidebar and click **Plan My Trip** to get started!")

    # Quick-start example destinations
    st.markdown("### 🌟 Popular Destinations")
    ex_cols = st.columns(5)
    examples = [
        ("🇯🇵", "Japan"), ("🇫🇷", "France"), ("🇹🇭", "Thailand"),
        ("🇮🇹", "Italy"), ("🇧🇷", "Brazil"),
    ]
    for i, (flag, country) in enumerate(examples):
        with ex_cols[i]:
            if st.button(f"{flag} {country}", key=f"ex_{country}", use_container_width=True):
                st.session_state.destination_input = country
                st.rerun()

# ── Main Content: Triggered on Search ────────────────────────────────────────
if search_btn and destination.strip():
    # Clear cached data if destination changed
    if st.session_state.searched_destination != destination.strip().lower():
        st.session_state.country_data = None
        st.session_state.weather_data = None
        st.session_state.images_data = None

    # ── Load Country Data ────────────────────────────────────────────────────
    if st.session_state.country_data is None:
        with st.spinner(f"🌍 Fetching details for {destination}..."):
            try:
                st.session_state.country_data = get_country_info(destination)
                st.session_state.searched_destination = destination.strip().lower()
            except Exception as e:
                st.error(f"❌ {e}")
                st.stop()

    # ── Load Weather Data ────────────────────────────────────────────────────
    country = st.session_state.country_data
    if st.session_state.weather_data is None:
        with st.spinner("🌤️ Loading weather forecast..."):
            try:
                st.session_state.weather_data = get_weather(country["lat"], country["lon"])
            except Exception as e:
                st.warning(f"⚠️ Weather unavailable: {e}")
                st.session_state.weather_data = {}

    # ── Load Images ──────────────────────────────────────────────────────────
    if st.session_state.images_data is None:
        with st.spinner("📸 Loading destination photos..."):
            try:
                st.session_state.images_data = get_destination_images(
                    f"{destination} travel landscape", count=6
                )
            except Exception as e:
                st.warning(f"⚠️ Images unavailable: {e}")
                st.session_state.images_data = []

# ── Render Tabs if Data Exists ────────────────────────────────────────────────
if st.session_state.country_data:
    country = st.session_state.country_data
    weather = st.session_state.weather_data
    images = st.session_state.images_data or []

    # Determine country currency for converter default
    country_currency = (
        country["currencies"][0]["code"] if country.get("currencies") else "USD"
    )
    weather_desc = (
        weather.get("current", {}).get("description", "Unknown")
        if weather else "Unknown"
    )

    # ── Tab Layout ───────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🌍 Overview",
        "🌤️ Weather",
        "💱 Currency",
        "📸 Gallery",
        "🤖 AI Itinerary",
        "⚡ Advanced",
    ])

    # ── Tab 1: Country Overview ───────────────────────────────────────────────
    with tab1:
        render_country_card(country)

    # ── Tab 2: Weather ────────────────────────────────────────────────────────
    with tab2:
        if weather and weather.get("current"):
            render_weather_card(weather)
        else:
            st.warning("Weather data could not be loaded for this destination.")

    # ── Tab 3: Currency ───────────────────────────────────────────────────────
    with tab3:
        render_currency_card(country, default_amount=budget_inr)

    # ── Tab 4: Image Gallery ──────────────────────────────────────────────────
    with tab4:
        render_image_gallery(images, destination)
        if st.button("🔄 Refresh Photos", key="refresh_photos"):
            with st.spinner("Loading new photos..."):
                try:
                    st.session_state.images_data = get_destination_images(
                        f"{destination} travel landscape", count=6
                    )
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

    # ── Tab 5: AI Itinerary ───────────────────────────────────────────────────
    with tab5:
        clean_interests = [i.split(" ", 1)[1] if " " in i else i for i in interests]

        st.markdown(
            f"""
            <div style="padding:1rem; border-radius:10px;
                        background: rgba(99,102,241,0.1); border:1px solid rgba(99,102,241,0.3);
                        margin-bottom:1rem;">
                <b>🎯 Trip Summary</b><br>
                <span style="color:#94a3b8;">
                    {days}-day trip to <b style="color:#e2e8f0;">{destination}</b> ·
                    Budget: <b style="color:#60a5fa;">₹{budget_inr:,.0f} INR</b> ·
                    Interests: <b style="color:#a78bfa;">{', '.join(clean_interests)}</b>
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("🚀 Generate AI Itinerary", key="gen_itinerary", use_container_width=True):
            with st.spinner("✨ Crafting your personalized itinerary with Groq AI..."):
                try:
                    itinerary = generate_itinerary(
                        destination=destination,
                        budget_inr=budget_inr,
                        days=days,
                        interests=clean_interests,
                        currency_code=country_currency,
                    )
                    st.session_state["itinerary"] = itinerary
                except Exception as e:
                    st.error(f"❌ AI generation failed: {e}")

        if st.session_state.get("itinerary"):
            render_itinerary(st.session_state["itinerary"], destination, days)
            st.download_button(
                label="📥 Download Itinerary",
                data=st.session_state["itinerary"],
                file_name=f"{destination.lower().replace(' ', '_')}_{days}day_itinerary.md",
                mime="text/markdown",
                key="download_itinerary",
            )

    # ── Tab 6: Advanced Features ──────────────────────────────────────────────
    with tab6:
        adv_tab1, adv_tab2, adv_tab3 = st.tabs([
            "💰 Budget Analysis", "🎒 Packing List", "🗺️ Local Tips"
        ])

        with adv_tab1:
            if st.button("📊 Analyze My Budget", key="analyze_budget", use_container_width=True):
                with st.spinner("💰 Analyzing your budget..."):
                    try:
                        analysis = analyze_budget(destination, budget_inr, days)
                        st.session_state["budget_analysis"] = analysis
                    except Exception as e:
                        st.error(f"❌ {e}")
            if st.session_state.get("budget_analysis"):
                render_budget_analysis(
                    st.session_state["budget_analysis"], budget_inr, days
                )

        with adv_tab2:
            if st.button("🎒 Generate Packing List", key="gen_packing", use_container_width=True):
                with st.spinner("🎒 Building your packing list..."):
                    try:
                        packing = generate_packing_list(destination, days, weather_desc)
                        st.session_state["packing_list"] = packing
                    except Exception as e:
                        st.error(f"❌ {e}")
            if st.session_state.get("packing_list"):
                render_packing_list(st.session_state["packing_list"], destination)
                st.download_button(
                    label="📥 Download Packing List",
                    data=st.session_state["packing_list"],
                    file_name=f"{destination.lower().replace(' ', '_')}_packing_list.md",
                    mime="text/markdown",
                    key="download_packing",
                )

        with adv_tab3:
            if st.button("🗺️ Get Local Tips", key="gen_tips", use_container_width=True):
                with st.spinner("🗺️ Gathering local insider knowledge..."):
                    try:
                        clean_interests = [i.split(" ", 1)[1] if " " in i else i for i in interests]
                        tips = generate_local_tips(destination, clean_interests)
                        st.session_state["local_tips"] = tips
                    except Exception as e:
                        st.error(f"❌ {e}")
            if st.session_state.get("local_tips"):
                render_local_tips(st.session_state["local_tips"], destination)

elif search_btn and not destination.strip():
    st.error("Please enter a destination name.")
