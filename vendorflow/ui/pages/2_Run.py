"""Run page — start runs + live progress."""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import nest_asyncio
nest_asyncio.apply()

import streamlit as st

st.set_page_config(page_title="Run — VendorFlow AI")

if "profile" not in st.session_state:
    try:
        from core.profile import load_profile
        st.session_state["profile"] = load_profile("data/profile.json")
    except Exception:
        pass

if "vault" not in st.session_state:
    from core.document_vault import DocumentVault
    st.session_state["vault"] = DocumentVault()

from core.orchestrator import run_batch, check_portal_status
from core.profile import CompanyProfile
from core.document_vault import DocumentVault
from core.scoped_vault import get_portal_category
from core.report_generator import generate_run_report
from ui.styles import inject_css, page_header, section_header, render_sidebar_nav
from ui.components.status_card import render_status_card

inject_css(overlay_opacity="0.94")

with st.sidebar:
    render_sidebar_nav()

st.html(page_header("Run", "Configure portals and start autonomous onboarding."))

profile: CompanyProfile | None = st.session_state.get("profile")
vault: DocumentVault = st.session_state.get("vault")
preflight = st.session_state.get("preflight_report")

# ── SECTION 1 — Portal Configuration ──
st.html(section_header("Portal Queue"))

default_portals = (
    "IndiaMART|https://seller.indiamart.com\n"
    "TradeIndia|https://www.tradeindia.com/register\n"
    "GeM|https://mkp.gem.gov.in/registration"
)

portal_text = st.text_area("Enter portal URLs (one per line, format: Name|URL)", value=default_portals, height=150)

portal_list = []
for line in portal_text.strip().splitlines():
    line = line.strip()
    if "|" in line:
        name, url = line.split("|", 1)
        portal_list.append({"name": name.strip(), "url": url.strip()})

if portal_list:
    st.html('<p style="color:#9CA3AF;font-size:0.85rem;font-weight:500;margin:0.5rem 0;">Portal Preview:</p>')
    for p in portal_list:
        cat = get_portal_category(p["url"])
        st.html(f"""
        <div style="background:rgba(22, 27, 34, 0.95);
             border:1px solid #30363D;
             border-radius:8px;
             padding:1rem 1.25rem;
             margin-bottom:0.5rem;
             display:flex;align-items:center;justify-content:space-between;">
            <div>
                <div style="color:#F0F6FC;font-weight:500;
                     font-size:0.875rem;">
                     {p['name']}
                </div>
                <div style="color:#6E7681;font-size:0.8rem;
                     margin-top:2px;
                     font-family:'DM Mono',monospace;">
                     {p['url']}
                </div>
            </div>
            <span style="background:#21262D;
                  color:#8B949E;font-size:0.7rem;
                  font-weight:500;padding:3px 10px;
                  border-radius:50px;
                  text-transform:uppercase;
                  letter-spacing:0.06em;">
                  {cat}
            </span>
        </div>
        """)

can_run = profile is not None
if not can_run:
    st.info("Set up your profile first (Setup page).")
if preflight and not preflight.is_ready:
    st.info("Preflight has RED items. You can still proceed, but some portals may fail.")

st.html("""<style>div[data-testid="stButton"] > button[kind="primary"] {
    width: 100% !important; padding: 1rem !important; font-size: 1.1rem !important; font-weight: 700 !important;
}</style>""")

if st.button("Start Onboarding", disabled=not can_run, type="primary"):
    if not vault:
        vault = DocumentVault()
        st.session_state["vault"] = vault
    st.session_state["batch_running"] = True
    with st.spinner("Running onboarding agents... this may take 15-20 minutes"):
        result = asyncio.run(run_batch(portal_list, profile, vault))
    st.session_state["last_batch_result"] = result
    st.session_state["batch_running"] = False
    st.rerun()

# ── SECTION 2 — Results ──
batch_result = st.session_state.get("last_batch_result")
if batch_result:
    st.divider()
    st.html(section_header("Results"))
    st.html(f"""
    <div style="background:rgba(22, 27, 34, 0.95);
         border:1px solid #30363D;
         border-top:3px solid #00B4A6;
         border-radius:8px;
         padding:1.5rem;margin:1.5rem 0;">
        <div style="color:#F0F6FC;font-weight:600;
             font-size:1rem;margin-bottom:1rem;">
             Onboarding Complete
        </div>
        <div style="display:flex;gap:2rem;">
            <div>
                <div style="color:#8B949E;font-size:0.75rem;
                     text-transform:uppercase;
                     letter-spacing:0.08em;
                     margin-bottom:4px;">Submitted</div>
                <div style="color:#3FB950;
                     font-family:'DM Mono',monospace;
                     font-size:1.5rem;font-weight:500;">
                     {batch_result.success_count}
                </div>
            </div>
            <div>
                <div style="color:#8B949E;font-size:0.75rem;
                     text-transform:uppercase;
                     letter-spacing:0.08em;
                     margin-bottom:4px;">Failed</div>
                <div style="color:#F85149;
                     font-family:'DM Mono',monospace;
                     font-size:1.5rem;font-weight:500;">
                     {batch_result.fail_count}
                </div>
            </div>
            <div>
                <div style="color:#8B949E;font-size:0.75rem;
                     text-transform:uppercase;
                     letter-spacing:0.08em;
                     margin-bottom:4px;">Total Time</div>
                <div style="color:#C9D1D9;
                     font-family:'DM Mono',monospace;
                     font-size:1.5rem;font-weight:500;">
                     {batch_result.total_time_seconds / 60:.1f}m
                </div>
            </div>
        </div>
    </div>
    """)
    for r in batch_result.portal_results:
        cols = st.columns([3, 1])
        with cols[0]:
            render_status_card(r.portal_name, r.portal_url, r.status, r.reference_id, r.time_taken_seconds, r.error_message)
        with cols[1]:
            if r.status == "submitted":
                if st.button("Check Status", key=f"check_{r.portal_url}"):
                    with st.spinner("Checking..."):
                        new_status = asyncio.run(check_portal_status(r))
                    st.info(f"Status: {new_status}")
    try:
        pdf_path = generate_run_report(batch_result.run_id)
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Download Report (PDF)", data=f.read(),
                               file_name=f"vendorflow_report_{batch_result.run_id[:8]}.pdf", mime="application/pdf")
    except Exception as e:
        st.caption(f"Report generation skipped: {e}")
