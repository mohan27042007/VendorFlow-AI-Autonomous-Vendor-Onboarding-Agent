"""Reusable portal status card component."""

import os
import sys

_vendorflow_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _vendorflow_dir not in sys.path:
    sys.path.insert(0, _vendorflow_dir)

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
    status_config = {
        "queued":    ("Queued", "rgba(139,148,158,0.1)", "#8B949E", "rgba(139,148,158,0.2)"),
        "running":   ("Running", "rgba(88,166,255,0.1)", "#58A6FF", "rgba(88,166,255,0.2)"),
        "submitted": ("Submitted", "rgba(63,185,80,0.1)", "#3FB950", "rgba(63,185,80,0.2)"),
        "failed":    ("Failed", "rgba(248,81,73,0.1)", "#F85149", "rgba(248,81,73,0.2)"),
    }
    label, bg, color, border = status_config.get(
        status, ("Unknown", "rgba(139,148,158,0.1)", "#8B949E", "rgba(139,148,158,0.2)"))

    time_str = ""
    if time_taken:
        time_str = f'<div style="color:#C9D1D9;font-family:\\\'DM Mono\\\',monospace;font-size:0.875rem;font-weight:500;margin-top:6px;">{time_taken / 60:.1f}m</div>'

    ref_str = ""
    if reference_id:
        ref_str = f'<div style="color:#8B949E;font-size:0.75rem;margin-top:4px;"><span style="color:#6E7681;text-transform:uppercase;letter-spacing:0.06em;font-size:0.65rem;">Ref:</span> {reference_id}</div>'

    st.html(f"""
    <div style="background:rgba(22, 27, 34, 0.95);
         border:1px solid #30363D;
         border-radius:8px;
         padding:1.25rem 1.5rem;
         margin-bottom:0.75rem;">
        <div style="display:flex;align-items:flex-start;justify-content:space-between;">
            <div>
                <div style="color:#F0F6FC;font-weight:600;font-size:1rem;">{portal_name}</div>
                <div style="color:#6E7681;font-size:0.8rem;margin-top:2px;font-family:'DM Mono',monospace;">{portal_url}</div>
                {ref_str}
            </div>
            <div style="text-align:right;">
                <span style="background:{bg};color:{color};font-size:0.75rem;
                      font-weight:600;padding:3px 10px;border-radius:50px;
                      border:1px solid {border};">{label}</span>
                {time_str}
            </div>
        </div>
    </div>
    """)

    if error_message and status == "failed":
        with st.expander("Error details"):
            st.code(error_message)
