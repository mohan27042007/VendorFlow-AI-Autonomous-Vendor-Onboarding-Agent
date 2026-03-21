"""Run page — start runs + live progress."""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import nest_asyncio
nest_asyncio.apply()

import streamlit as st

from core.orchestrator import run_batch, check_portal_status
from core.profile import CompanyProfile
from core.document_vault import DocumentVault
from core.scoped_vault import get_portal_category
from core.report_generator import generate_run_report
from ui.components.status_card import render_status_card

st.header("🚀 Run")

# --- Session state ---
profile: CompanyProfile | None = st.session_state.get("profile")
vault: DocumentVault = st.session_state.get("vault")
preflight = st.session_state.get("preflight_report")

# ──────────────────────────────────────────────
# SECTION 1 — Portal Configuration
# ──────────────────────────────────────────────
st.subheader("Portal Queue")

default_portals = (
    "IndiaMART|https://seller.indiamart.com\n"
    "TradeIndia|https://www.tradeindia.com/register\n"
    "GeM|https://mkp.gem.gov.in/registration"
)

portal_text = st.text_area(
    "Enter portal URLs (one per line, format: Name|URL)",
    value=default_portals,
    height=150,
)

# Parse portals
portal_list = []
for line in portal_text.strip().splitlines():
    line = line.strip()
    if "|" in line:
        name, url = line.split("|", 1)
        portal_list.append({"name": name.strip(), "url": url.strip()})

if portal_list:
    st.markdown("**Preview:**")
    preview_data = []
    for i, p in enumerate(portal_list, 1):
        cat = get_portal_category(p["url"])
        preview_data.append({"#": i, "Portal Name": p["name"], "URL": p["url"], "Category": cat})
    st.dataframe(preview_data, use_container_width=True, hide_index=True)

can_run = profile is not None
if not can_run:
    st.warning("Set up your profile first (Setup page).")

if preflight and not preflight.is_ready:
    st.warning("Preflight has RED items. You can still proceed, but some portals may fail.")

start_disabled = not can_run
if st.button("Start Onboarding", disabled=start_disabled, type="primary"):
    if not vault:
        vault = DocumentVault()
        st.session_state["vault"] = vault

    st.session_state["batch_running"] = True

    with st.spinner("Running onboarding agents... this may take 15-20 minutes"):
        result = asyncio.run(run_batch(portal_list, profile, vault))

    st.session_state["last_batch_result"] = result
    st.session_state["batch_running"] = False
    st.rerun()

# ──────────────────────────────────────────────
# SECTION 2 — Results
# ──────────────────────────────────────────────
batch_result = st.session_state.get("last_batch_result")

if batch_result:
    st.divider()
    st.subheader("Results")

    st.markdown(
        f"**{batch_result.success_count} portals submitted | "
        f"{batch_result.fail_count} failed | "
        f"{batch_result.total_time_seconds / 60:.1f} minutes total**"
    )

    for r in batch_result.portal_results:
        cols = st.columns([3, 1])
        with cols[0]:
            render_status_card(
                portal_name=r.portal_name,
                portal_url=r.portal_url,
                status=r.status,
                reference_id=r.reference_id,
                time_taken=r.time_taken_seconds,
                error_message=r.error_message,
            )
        with cols[1]:
            if r.status == "submitted":
                if st.button("Check Status", key=f"check_{r.portal_url}"):
                    with st.spinner("Checking..."):
                        new_status = asyncio.run(check_portal_status(r))
                    st.info(f"Status: {new_status}")

    # PDF download
    try:
        pdf_path = generate_run_report(batch_result.run_id)
        with open(pdf_path, "rb") as f:
            st.download_button(
                "📥 Download Report (PDF)",
                data=f.read(),
                file_name=f"vendorflow_report_{batch_result.run_id[:8]}.pdf",
                mime="application/pdf",
            )
    except Exception as e:
        st.caption(f"Report generation skipped: {e}")
