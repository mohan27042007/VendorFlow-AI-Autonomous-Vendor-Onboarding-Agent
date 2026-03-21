"""ROI metrics widget component."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st


def render_roi_widget(
    portals_completed: int,
    ai_time_hours: float,
    manual_hours_per_portal: float = 2.5,
    hourly_rate: float = 25.0,
) -> None:
    """Render the ROI comparison box."""
    hours_saved = portals_completed * manual_hours_per_portal
    cost_saved = hours_saved * hourly_rate
    time_diff = hours_saved - ai_time_hours

    st.info(
        f"**🤖 VendorFlow AI:** {portals_completed} portals "
        f"in {ai_time_hours:.1f} hours\n\n"
        f"**👤 Manual equivalent:** {hours_saved:.1f} hours\n\n"
        f"**💰 You saved:** ${cost_saved:,.0f} "
        f"({time_diff:.1f} hours)"
    )
