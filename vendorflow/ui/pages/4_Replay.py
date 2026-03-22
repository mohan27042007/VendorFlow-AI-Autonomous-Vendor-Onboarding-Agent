"""Replay page — time-lapse screenshot viewer."""

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
from PIL import Image

st.set_page_config(page_title="Replay — VendorFlow AI")

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
from config.settings import SCREENSHOTS_DIR
from ui.styles import inject_css, page_header, render_sidebar_nav

inject_css(overlay_opacity="0.94")

with st.sidebar:
    render_sidebar_nav()

st.html(page_header("Replay", "Review agent actions from past runs."))

# ── Run Selection ──
history = db.get_run_history()

if not history:
    st.html("""
    <div style="background:rgba(22, 27, 34, 0.95);border:1px solid #30363D;border-radius:8px;padding:3rem;text-align:center;">
        <div style="color:#30363D;font-size:2rem;margin-bottom:1rem;">[ ]</div>
        <div style="color:#C9D1D9;font-weight:500;margin-bottom:0.5rem;">No screenshots captured</div>
        <div style="color:#8B949E;font-size:0.875rem;">Screenshots will appear here after future runs.</div>
    </div>
    """)
    st.stop()

seen = {}
for r in history:
    rid = r["run_id"]
    if rid not in seen:
        seen[rid] = r.get("started_at", "")[:10]

run_options = {f"{rid[:8]} — {date}": rid for rid, date in seen.items()}
selected_label = st.selectbox("Select a run", options=list(run_options.keys()))
actual_run_id = run_options[selected_label]

# ── Portal Selection ──
portals = db.get_portals_for_run(actual_run_id)
if not portals:
    st.info("No portal results for this run.")
    st.stop()

portal_names = [p["portal_name"] for p in portals]
selected_portal_name = st.selectbox("Select a portal", options=portal_names)
selected_portal = next(p for p in portals if p["portal_name"] == selected_portal_name)

# ── Screenshot Replay ──
screenshot_dir = selected_portal.get("screenshot_dir")

if not screenshot_dir or not os.path.isdir(screenshot_dir):
    st.html("""
    <div style="background:rgba(22, 27, 34, 0.95);border:1px solid #30363D;border-radius:8px;padding:3rem;text-align:center;">
        <div style="color:#30363D;font-size:2rem;margin-bottom:1rem;">[ ]</div>
        <div style="color:#C9D1D9;font-weight:500;margin-bottom:0.5rem;">No screenshots captured for this run.</div>
        <div style="color:#8B949E;font-size:0.875rem;">Screenshots will appear here after future runs.</div>
    </div>
    """)
    st.stop()

image_files = sorted(glob.glob(os.path.join(screenshot_dir, "*.png")) + glob.glob(os.path.join(screenshot_dir, "*.jpg")))

if not image_files:
    st.html("""
    <div style="background:rgba(22, 27, 34, 0.95);border:1px solid #30363D;border-radius:8px;padding:3rem;text-align:center;">
        <div style="color:#30363D;font-size:2rem;margin-bottom:1rem;">[ ]</div>
        <div style="color:#C9D1D9;font-weight:500;margin-bottom:0.5rem;">No screenshots found in directory.</div>
        <div style="color:#8B949E;font-size:0.875rem;">Screenshots will appear here after future runs.</div>
    </div>
    """)
    st.stop()

st.html(f'<p style="color:#9CA3AF;font-size:0.85rem;">{len(image_files)} screenshots captured</p>')

frame_index = st.slider("Frame", min_value=0, max_value=len(image_files) - 1, value=0)

img = Image.open(image_files[frame_index])
if img.width > 800:
    ratio = 800 / img.width
    img = img.resize((800, int(img.height * ratio)))

st.html('<div style="background:#111827;border:1px solid #374151;border-radius:16px;padding:1rem;margin-top:1rem;">')
st.image(img, caption=f"Frame {frame_index + 1} of {len(image_files)} — {selected_portal_name}", use_container_width=False)
st.html('</div>')

st.html(f'<div style="text-align:center;color:#9CA3AF;font-size:0.85rem;margin-top:0.5rem;">Frame {frame_index + 1} of {len(image_files)} — {selected_portal_name}</div>')
