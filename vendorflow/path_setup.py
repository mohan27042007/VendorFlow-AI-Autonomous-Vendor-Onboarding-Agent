"""Path setup helper for Streamlit Cloud compatibility."""

import os
import sys


def setup_vendorflow_path():
    """Find and add vendorflow directory to sys.path."""
    # Walk up from current file to find vendorflow/ or config/settings.py
    path = os.path.abspath(__file__)
    for _ in range(6):
        path = os.path.dirname(path)
        if os.path.exists(os.path.join(path, "config", "settings.py")):
            if path not in sys.path:
                sys.path.insert(0, path)
            return path
    # Fallback: try relative to this file
    fallback = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if fallback not in sys.path:
        sys.path.insert(0, fallback)
    return fallback
