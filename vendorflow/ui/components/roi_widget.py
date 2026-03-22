"""ROI metrics widget component."""

import os
import sys

_vendorflow_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _vendorflow_dir not in sys.path:
    sys.path.insert(0, _vendorflow_dir)

import streamlit as st


def render_roi_widget(
    portals_completed: int,
    ai_time_hours: float,
    manual_hours_per_portal: float = 2.5,
    hourly_rate: float = 25.0,
) -> None:
    """Render the dramatic 3-panel ROI comparison."""
    hours_saved = portals_completed * manual_hours_per_portal
    cost_saved = hours_saved * hourly_rate
    hours_diff = hours_saved - ai_time_hours

    st.html(f"""
    <div style="background:rgba(22, 27, 34, 0.95);
         border:1px solid #30363D;
         border-radius:8px;
         padding:1.5rem;margin:1rem 0;">
        <div style="color:#8B949E;font-size:0.75rem;
             font-weight:500;text-transform:uppercase;
             letter-spacing:0.1em;margin-bottom:1.5rem;">
             Time & Cost Analysis
        </div>
        <div style="display:grid;
             grid-template-columns:1fr 1fr 1fr;
             gap:1rem;">
             
            <!-- VendorFlow AI panel -->
            <div style="background:#0D1117;
                 border:1px solid #21262D;
                 border-top:2px solid #00B4A6;
                 border-radius:6px;padding:1.25rem;">
                <div style="color:#8B949E;font-size:0.7rem;
                     text-transform:uppercase;
                     letter-spacing:0.1em;
                     margin-bottom:0.75rem;">
                     VendorFlow AI
                </div>
                <div style="color:#00B4A6;
                     font-family:'DM Mono',monospace;
                     font-size:2rem;font-weight:500;">
                     {ai_time_hours:.1f}h
                </div>
                <div style="color:#6E7681;
                     font-size:0.8rem;margin-top:4px;">
                     {portals_completed} portals
                </div>
            </div>
            
            <!-- Manual panel -->
            <div style="background:#0D1117;
                 border:1px solid #21262D;
                 border-top:2px solid #F85149;
                 border-radius:6px;padding:1.25rem;">
                <div style="color:#8B949E;font-size:0.7rem;
                     text-transform:uppercase;
                     letter-spacing:0.1em;
                     margin-bottom:0.75rem;">
                     Manual Work
                </div>
                <div style="color:#F85149;
                     font-family:'DM Mono',monospace;
                     font-size:2rem;font-weight:500;">
                     {hours_saved:.1f}h
                </div>
                <div style="color:#6E7681;
                     font-size:0.8rem;margin-top:4px;">
                     estimated
                </div>
            </div>
            
            <!-- Savings panel -->
            <div style="background:#0D1117;
                 border:1px solid #21262D;
                 border-top:2px solid #3FB950;
                 border-radius:6px;padding:1.25rem;">
                <div style="color:#8B949E;font-size:0.7rem;
                     text-transform:uppercase;
                     letter-spacing:0.1em;
                     margin-bottom:0.75rem;">
                     You Saved
                </div>
                <div style="color:#3FB950;
                     font-family:'DM Mono',monospace;
                     font-size:2rem;font-weight:500;">
                     ${cost_saved:,.0f}
                </div>
                <div style="color:#6E7681;
                     font-size:0.8rem;margin-top:4px;">
                     {hours_diff:.1f} hours back
                </div>
            </div>
            
        </div>
    </div>
    """)
