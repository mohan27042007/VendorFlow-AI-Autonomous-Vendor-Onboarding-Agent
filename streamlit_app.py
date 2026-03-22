"""Streamlit Cloud entry point — sets up path and launches app."""

import sys
import os

vendorflow_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendorflow")
sys.path.insert(0, vendorflow_path)
os.chdir(vendorflow_path)

import streamlit as st

home = st.Page("vendorflow/ui/app.py", title="Home", default=True)
setup = st.Page("vendorflow/ui/pages/1_Setup.py", title="Setup")
run = st.Page("vendorflow/ui/pages/2_Run.py", title="Run")
dashboard = st.Page("vendorflow/ui/pages/3_Dashboard.py", title="Dashboard")
replay = st.Page("vendorflow/ui/pages/4_Replay.py", title="Replay")

pg = st.navigation([home, setup, run, dashboard, replay])
pg.run()
