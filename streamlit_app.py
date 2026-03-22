"""Streamlit Cloud entry point — sets up path and launches app."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "vendorflow"))

from ui.app import *
