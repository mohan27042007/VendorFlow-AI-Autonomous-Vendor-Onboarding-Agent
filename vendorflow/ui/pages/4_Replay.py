"""Replay page — time-lapse screenshot viewer."""

import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from PIL import Image

import db.database as db
from config.settings import SCREENSHOTS_DIR

st.header("▶️ Replay")

# ──────────────────────────────────────────────
# SECTION 1 — Run Selection
# ──────────────────────────────────────────────
history = db.get_run_history()

if not history:
    st.info("No runs yet.")
    st.stop()

seen = {}
for r in history:
    rid = r["run_id"]
    if rid not in seen:
        seen[rid] = r.get("started_at", "")[:10]

run_options = {f"{rid[:8]} — {date}": rid for rid, date in seen.items()}
selected_label = st.selectbox("Select a run", options=list(run_options.keys()))
actual_run_id = run_options[selected_label]

# ──────────────────────────────────────────────
# SECTION 2 — Portal Selection
# ──────────────────────────────────────────────
portals = db.get_portals_for_run(actual_run_id)

if not portals:
    st.info("No portal results for this run.")
    st.stop()

portal_names = [p["portal_name"] for p in portals]
selected_portal_name = st.selectbox("Select a portal", options=portal_names)

selected_portal = next(p for p in portals if p["portal_name"] == selected_portal_name)

# ──────────────────────────────────────────────
# SECTION 3 — Screenshot Replay
# ──────────────────────────────────────────────
screenshot_dir = selected_portal.get("screenshot_dir")

if not screenshot_dir or not os.path.isdir(screenshot_dir):
    st.info("No screenshots captured for this run.")
    st.stop()

image_files = sorted(
    glob.glob(os.path.join(screenshot_dir, "*.png"))
    + glob.glob(os.path.join(screenshot_dir, "*.jpg"))
)

if not image_files:
    st.info("No screenshots found in this run's directory.")
    st.stop()

st.caption(f"{len(image_files)} screenshots captured")

frame_index = st.slider("Frame", min_value=0, max_value=len(image_files) - 1, value=0)

img = Image.open(image_files[frame_index])
if img.width > 800:
    ratio = 800 / img.width
    img = img.resize((800, int(img.height * ratio)))

st.image(img, caption=f"Frame {frame_index + 1} of {len(image_files)}", use_container_width=False)
