"""Streamlit Cloud entry point — sets up path and launches app."""

import os
import sys

# Add vendorflow to path
vendorflow_path = os.path.join(os.path.dirname(__file__), "vendorflow")
sys.path.insert(0, vendorflow_path)

# Change working directory to vendorflow so relative paths resolve
os.chdir(vendorflow_path)

# Now import and run the app
from ui.app import *
