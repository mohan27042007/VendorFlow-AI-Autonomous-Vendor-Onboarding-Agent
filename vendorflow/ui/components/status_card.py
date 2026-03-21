"""Reusable portal status card component."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st


def render_status_card(
    portal_name: str,
    portal_url: str,
    status: str,
    reference_id: str | None = None,
    time_taken: float | None = None,
    error_message: str | None = None,
) -> None:
    """Render a colored status card for a portal run."""
    status_map = {
        "queued": ("⏳ Queued", "gray"),
        "running": ("🔄 Running", "blue"),
        "submitted": ("✅ Submitted", "green"),
        "failed": ("❌ Failed", "red"),
    }
    label, color = status_map.get(status, ("❓ Unknown", "gray"))

    with st.container(border=True):
        st.markdown(f"**{portal_name}**")
        st.caption(portal_url)
        st.markdown(f":{color}[{label}]")

        if reference_id:
            st.text(f"Reference: {reference_id}")
        if time_taken is not None:
            st.text(f"Time: {time_taken / 60:.1f} min")
        if error_message and status == "failed":
            with st.expander("Error details"):
                st.code(error_message)
