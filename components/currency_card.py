"""currency_card.py — Renders currency conversion UI."""

import streamlit as st
from services.currency import convert_currency, get_popular_conversions, POPULAR_CURRENCIES


def render_currency_card(country_info: dict, default_amount: float = 50000.0):
    """Display currency conversion with popular travel currencies."""
    # Determine target currency from country info
    target_code = "USD"
    if country_info.get("currencies"):
        target_code = country_info["currencies"][0]["code"]

    st.markdown("### 💱 Currency Converter")

    col_in, col_out = st.columns(2)
    with col_in:
        amount = st.number_input(
            "Amount (INR ₹)",
            min_value=0.0,
            max_value=10_000_000.0,
            value=default_amount,
            step=1000.0,
            format="%.0f",
            key="currency_amount",
        )
    with col_out:
        # Build selectable list
        all_codes = POPULAR_CURRENCIES[:]
        if target_code not in all_codes:
            all_codes.insert(0, target_code)
        default_idx = all_codes.index(target_code) if target_code in all_codes else 0
        to_currency = st.selectbox(
            "Convert To",
            options=all_codes,
            index=default_idx,
            key="currency_target",
        )

    if st.button("🔄 Convert", key="convert_btn", use_container_width=True):
        with st.spinner("Fetching live rates..."):
            try:
                result = convert_currency(amount, "INR", to_currency)
                st.markdown(
                    f"""
                    <div style="text-align:center; padding:2rem; border-radius:12px;
                                background: linear-gradient(135deg, #1e3a5f, #0f2547);
                                border: 1px solid #3b82f6; margin: 1rem 0;">
                        <div style="font-size:1rem; color:#94a3b8; margin-bottom:0.5rem;">
                            {result['formatted_from']} INR equals
                        </div>
                        <div style="font-size:3rem; font-weight:800; color:#60a5fa;">
                            {result['formatted_to']}
                        </div>
                        <div style="font-size:0.85rem; color:#64748b; margin-top:0.5rem;">
                            1 INR = {result['rate']:.4f} {result['to_currency']}
                        </div>
                        <div style="font-size:0.75rem; color:#475569; margin-top:0.3rem;">
                            Last updated: {result['last_updated']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.error(f"Conversion failed: {e}")

    # Popular currencies table
    st.divider()
    st.markdown("### 🌍 Popular Travel Currencies")
    st.caption(f"Showing equivalent of ₹{amount:,.0f} INR")

    with st.spinner("Loading rates..."):
        try:
            conversions = get_popular_conversions(amount, "INR")
            cols = st.columns(4)
            for i, conv in enumerate(conversions[:16]):
                with cols[i % 4]:
                    st.markdown(
                        f"""
                        <div style="padding:0.6rem; border-radius:8px; margin-bottom:0.5rem;
                                    background: rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);
                                    text-align:center;">
                            <div style="font-size:0.7rem; color:#94a3b8; font-weight:600;">{conv['currency']}</div>
                            <div style="font-size:1rem; font-weight:700; color:#e2e8f0;">{conv['formatted']}</div>
                            <div style="font-size:0.65rem; color:#475569;">rate: {conv['rate']:.4f}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        except Exception as e:
            st.warning(f"Could not load all rates: {e}")
