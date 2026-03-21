"""Streamlit entry point for VendorFlow AI."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from config.settings import TINYFISH_API_KEY

st.set_page_config(
    page_title="VendorFlow AI",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.markdown("# 🐟 VendorFlow AI")
    st.caption("Autonomous Vendor Onboarding")
    st.divider()
    st.page_link("pages/1_Setup.py", label="Setup", icon="⚙️")
    st.page_link("pages/2_Run.py", label="Run", icon="🚀")
    st.page_link("pages/3_Dashboard.py", label="Dashboard", icon="📊")
    st.page_link("pages/4_Replay.py", label="Replay", icon="▶️")
    st.divider()

    if TINYFISH_API_KEY and TINYFISH_API_KEY != "your_api_key_here":
        st.markdown(":green[● API Connected]")
    else:
        st.markdown(":red[● API Not Connected]")

st.markdown("# VendorFlow AI")
st.markdown("### Autonomous Vendor Onboarding Agent")
st.divider()

col1, col2, col3 = st.columns(3)
col1.metric("Portals Supported", "5+")
col2.metric("Avg Time Saved", "2-4 hrs/portal")
col3.metric("Powered By", "TinyFish")

st.divider()
st.info("→ Go to **Setup** to configure your company profile, then **Run** to start onboarding.")
