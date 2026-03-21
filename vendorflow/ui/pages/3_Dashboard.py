"""Dashboard page — ROI dashboard + What If widget."""

import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st

import db.database as db
from config.settings import BLUEPRINTS_DIR
from core.blueprint import load_blueprint
from ui.components.roi_widget import render_roi_widget

st.header("📊 Dashboard")

# ──────────────────────────────────────────────
# SECTION 1 — ROI Metrics
# ──────────────────────────────────────────────
history = db.get_run_history()

total_portals_completed = sum(r.get("success_count", 0) or 0 for r in history)
total_runs = len(set(r["run_id"] for r in history)) if history else 0

submitted_times = [
    r["time_taken_seconds"]
    for r in history
    if r.get("status") == "submitted" and r.get("time_taken_seconds")
]
avg_time = (sum(submitted_times) / len(submitted_times) / 60) if submitted_times else 0

blueprint_count = len(glob.glob(os.path.join(BLUEPRINTS_DIR, "*.json")))

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Portals Completed", total_portals_completed)
col2.metric("Total Runs", total_runs)
col3.metric("Avg Time Per Portal", f"{avg_time:.1f} min")
col4.metric("Blueprints Learned", blueprint_count)

st.divider()

# ──────────────────────────────────────────────
# SECTION 2 — "What If Manual?" Simulator
# ──────────────────────────────────────────────
st.subheader("What If Manual? Simulator")

c1, c2 = st.columns(2)
with c1:
    manual_hours = st.slider("Manual hours per portal", min_value=1.0, max_value=8.0, value=2.5, step=0.5)
with c2:
    hourly_rate = st.slider("Hourly cost (USD)", min_value=10, max_value=100, value=25, step=5)

ai_time_hours = sum(submitted_times) / 3600 if submitted_times else 0

render_roi_widget(
    portals_completed=total_portals_completed,
    ai_time_hours=ai_time_hours,
    manual_hours_per_portal=manual_hours,
    hourly_rate=float(hourly_rate),
)

st.divider()

# ──────────────────────────────────────────────
# SECTION 3 — Run History Table
# ──────────────────────────────────────────────
st.subheader("Run History")

if history:
    seen_runs = {}
    for r in history:
        rid = r["run_id"]
        if rid not in seen_runs:
            seen_runs[rid] = {
                "Run ID": rid[:8],
                "Started": (r.get("started_at") or "")[:16],
                "Portals": r.get("portal_count", 0),
                "Success": r.get("success_count", 0),
                "Total Time (s)": round(r.get("total_time_seconds", 0) or 0, 1),
                "Status": "Completed" if r.get("completed_at") else "Running",
            }
    st.dataframe(list(seen_runs.values()), use_container_width=True, hide_index=True)
else:
    st.info("No runs yet. Go to Run page to start.")

st.divider()

# ──────────────────────────────────────────────
# SECTION 4 — Blueprint Library
# ──────────────────────────────────────────────
st.subheader("Portal Blueprint Library")

blueprint_files = glob.glob(os.path.join(BLUEPRINTS_DIR, "*.json"))
if blueprint_files:
    bp_data = []
    for f in blueprint_files:
        domain = os.path.splitext(os.path.basename(f))[0]
        bp = load_blueprint(domain)
        if bp:
            bp_data.append({
                "Portal": bp.portal_name,
                "Domain": bp.domain,
                "Success Count": bp.success_count,
                "Last Success": bp.last_success_date[:16],
            })
    if bp_data:
        st.dataframe(bp_data, use_container_width=True, hide_index=True)
    else:
        st.info("No blueprints loaded.")
else:
    st.info("No blueprints yet. Blueprints are created automatically after successful runs.")
