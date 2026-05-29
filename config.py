"""
config.py — Centralised secret/config loader.
Reads from st.secrets (Streamlit Cloud) first, then .env file.
"""

import os
from dotenv import load_dotenv

load_dotenv()


def get_secret(key: str, default: str = "") -> str:
    """
    Read a secret from Streamlit secrets (Cloud) or .env (local).
    Priority: st.secrets → os.environ → default
    """
    # Try Streamlit secrets first (works on Streamlit Cloud)
    try:
        import streamlit as st
        val = st.secrets.get(key, "")
        if val:
            return str(val)
    except Exception:
        pass

    # Fall back to environment variable / .env file
    return os.getenv(key, default)
