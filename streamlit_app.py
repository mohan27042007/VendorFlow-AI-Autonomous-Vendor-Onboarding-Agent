"""Streamlit Cloud entry point — sets up path and launches app."""

import sys
import os

vendorflow_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendorflow")
sys.path.insert(0, vendorflow_path)
os.chdir(vendorflow_path)

import streamlit as st

pages = [
    st.Page("vendorflow/ui/pages/1_Setup.py", title="Setup"),
    st.Page("vendorflow/ui/pages/2_Run.py", title="Run"),
    st.Page("vendorflow/ui/pages/3_Dashboard.py", title="Dashboard"),
    st.Page("vendorflow/ui/pages/4_Replay.py", title="Replay"),
]

pg = st.navigation(pages)
pg.run()
