"""image_gallery.py — Renders destination image gallery."""

import streamlit as st


def render_image_gallery(images: list[dict], destination: str):
    """Display a responsive image grid with attribution."""
    if not images:
        st.warning("No images found for this destination.")
        return

    st.markdown(f"### 📸 {destination} — Photo Gallery")

    # 3-column masonry-style grid
    cols = st.columns(3)
    for i, img in enumerate(images):
        with cols[i % 3]:
            st.image(
                img["url"],
                caption=f"📷 {img['photographer']} · {img['source']}",
                use_container_width=True,
            )
            st.markdown(
                f"<div style='text-align:center; margin-bottom:1rem;'>"
                f"<a href='{img['source_link']}' target='_blank' "
                f"style='font-size:0.7rem; color:#60a5fa; text-decoration:none;'>"
                f"View on {img['source']} ↗</a></div>",
                unsafe_allow_html=True,
            )

    # Attribution note
    sources = list({img["source"] for img in images})
    st.caption(f"Images sourced from: {', '.join(sources)}. All rights belong to respective photographers.")
