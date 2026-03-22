"""Dashboard page — ROI dashboard + What If widget."""

import glob
import os
import sys

_vendorflow_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _vendorflow_dir not in sys.path:
    sys.path.insert(0, _vendorflow_dir)
_path = os.path.abspath(__file__)
for _ in range(5):
    _path = os.path.dirname(_path)
    if os.path.exists(os.path.join(_path, "config", "settings.py")):
        if _path not in sys.path:
            sys.path.insert(0, _path)
        break

import streamlit as st
import time

st.set_page_config(page_title="Dashboard — VendorFlow AI")

if "profile" not in st.session_state:
    try:
        from core.profile import load_profile
        st.session_state["profile"] = load_profile("data/profile.json")
    except Exception:
        pass

if "vault" not in st.session_state:
    from core.document_vault import DocumentVault
    st.session_state["vault"] = DocumentVault()

import db.database as db
from config.settings import BLUEPRINTS_DIR
from core.blueprint import load_blueprint
from ui.styles import inject_css, page_header, section_header, render_sidebar_nav
from ui.components.roi_widget import render_roi_widget

inject_css(overlay_opacity="0.94")

with st.sidebar:
    render_sidebar_nav()

st.html(page_header("Dashboard", "Performance metrics, ROI analysis, and portal blueprints."))

# ── SECTION 1 — ROI Metrics ──
skeleton_placeholder = st.empty()
with skeleton_placeholder:
    st.html(("<div style='background:linear-gradient(90deg,#111827 25%,#1F2937 50%,#111827 75%);"
             "background-size:200% 100%;animation:shimmer 1.5s infinite;"
             "border-radius:8px;height:48px;margin-bottom:8px;'></div>") * 5)

time.sleep(0.5)
history = db.get_run_history()
skeleton_placeholder.empty()

total_portals_completed = sum(r.get("success_count", 0) or 0 for r in history)

if total_portals_completed == 0:
    st.html("""
    <div style="background:rgba(22, 27, 34, 0.95);border:1px solid #30363D;
         border-radius:8px;padding:3rem;text-align:center;
         margin:2rem 0;">
        <div style="color:#30363D;font-size:2rem;margin-bottom:1rem;">[ ]</div>
        <div style="color:#C9D1D9;font-weight:500;
             font-size:1.1rem;margin-bottom:0.5rem;">
             No runs yet
        </div>
        <div style="color:#8B949E;font-size:0.875rem;">
             Go to the Run page to start your first onboarding session.
        </div>
    </div>
    """)
    st.stop()

total_runs = len(set(r["run_id"] for r in history)) if history else 0
submitted_times = [r["time_taken_seconds"] for r in history if r.get("status") == "submitted" and r.get("time_taken_seconds")]
avg_time = (sum(submitted_times) / len(submitted_times) / 60) if submitted_times else 0
blueprint_count = len(glob.glob(os.path.join(BLUEPRINTS_DIR, "*.json")))

metrics = [
    ("TOTAL PORTALS COMPLETED", str(total_portals_completed)),
    ("TOTAL RUNS", str(total_runs)),
    ("AVG TIME PER PORTAL", f"{avg_time:.1f} min"),
    ("BLUEPRINTS LEARNED", str(blueprint_count)),
]

cols = st.columns(4)
for col, (label, value) in zip(cols, metrics):
    with col:
        num_val = value.replace(" min", "")
        suffix = " min" if "min" in value else ""
        counter_attrs = f'class="counter" data-target="{num_val}"' if num_val.replace(".", "").isdigit() else ""
        st.html(f"""
        <div style="background:rgba(22, 27, 34, 0.95);
             border:1px solid #30363D;
             border-radius:8px;
             padding:1.5rem;">
            <div style="color:#8B949E;font-size:0.75rem;
                 font-weight:500;text-transform:uppercase;
                 letter-spacing:0.1em;margin-bottom:0.75rem;">
                 {label}
            </div>
            <div style="color:#F0F6FC;
                 font-family:'DM Mono',monospace;
                 font-size:2.25rem;font-weight:500;
                 line-height:1;">
                 <span {counter_attrs}>{num_val}</span><span style="font-family:'DM Sans',sans-serif;font-size:1.25rem;margin-left:2px;color:#8B949E;">{suffix}</span>
            </div>
        </div>
        """)

st.divider()

# ── SECTION 2 — What If Manual? ──
st.html(section_header("What If Manual? Simulator"))
c1, c2 = st.columns(2)
with c1:
    manual_hours = st.slider("Manual hours per portal", min_value=1.0, max_value=8.0, value=2.5, step=0.5)
with c2:
    hourly_rate = st.slider("Hourly cost (USD)", min_value=10, max_value=100, value=25, step=5)
ai_time_hours = sum(submitted_times) / 3600 if submitted_times else 0
render_roi_widget(total_portals_completed, ai_time_hours, manual_hours, float(hourly_rate))

st.divider()

# ── SECTION 3 — Run History ──
st.html(section_header("Run History"))
if history:
    seen_runs = {}
    for r in history:
        rid = r["run_id"]
        if rid not in seen_runs:
            seen_runs[rid] = {"Run ID": rid[:8], "Started": (r.get("started_at") or "")[:16],
                              "Portals": r.get("portal_count", 0), "Success": r.get("success_count", 0),
                              "Total Time (s)": round(r.get("total_time_seconds", 0) or 0, 1),
                              "Status": "Completed" if r.get("completed_at") else "Running"}
    st.dataframe(list(seen_runs.values()), use_container_width=True, hide_index=True)
else:
    st.info("No runs yet. Go to Run page to start.")

st.divider()

# ── SECTION 4 — Blueprint Library ──
st.html(section_header("Portal Blueprint Library"))
blueprint_files = glob.glob(os.path.join(BLUEPRINTS_DIR, "*.json"))
if blueprint_files:
    for f in blueprint_files:
        domain = os.path.splitext(os.path.basename(f))[0]
        bp = load_blueprint(domain)
        if bp:
            st.html(f"""
        <div style="background:rgba(22, 27, 34, 0.95);
             border:1px solid #30363D;
             border-radius:8px;
             padding:1.25rem 1.5rem;
             margin-bottom:0.75rem;
             display:flex;align-items:center;justify-content:space-between;">
            <div>
                <div style="color:#F0F6FC;font-weight:600;font-size:1rem;display:flex;align-items:center;">
                    <div style="width:8px;height:8px;background:#00B4A6;border-radius:50%;display:inline-block;margin-right:8px;"></div>
                    {bp.portal_name}
                </div>
                <div style="color:#6E7681;font-size:0.8rem;margin-top:2px;margin-left:16px;font-family:'DM Mono',monospace;">{bp.domain}</div>
            </div>
            <div style="text-align:right;">
                <div style="color:#3FB950;font-weight:500;font-size:0.875rem;">{bp.success_count} successful runs</div>
                <div style="color:#8B949E;font-size:0.75rem;margin-top:4px;">Last: {bp.last_success_date[:10]}</div>
            </div>
        </div>
            """)
else:
    st.info("No blueprints yet. Blueprints are created automatically after successful runs.")
