"""Setup page — profile input + document upload + preflight."""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from pydantic import ValidationError

st.set_page_config(page_title="Setup — VendorFlow AI")

from core.document_vault import DocumentType, DocumentVault
from core.preflight import run_preflight
from core.profile import CompanyProfile, load_profile, save_profile
from ui.styles import inject_css, page_header, section_header, render_sidebar_nav

inject_css(overlay_opacity="0.94")

with st.sidebar:
    render_sidebar_nav()

st.html(page_header("Setup", "Configure your company profile and compliance documents."))

# --- Init session state ---
if "profile" not in st.session_state:
    try:
        st.session_state["profile"] = load_profile("data/profile.json")
    except Exception:
        st.session_state["profile"] = None

if "vault" not in st.session_state:
    st.session_state["vault"] = DocumentVault()

if "preflight_report" not in st.session_state:
    st.session_state["preflight_report"] = None

profile: CompanyProfile | None = st.session_state.get("profile")
vault: DocumentVault = st.session_state["vault"]

# ── SECTION 1 — Company Profile ──
st.html(section_header("Company Profile", badge="Required"))

defaults = {}
if profile:
    defaults = profile.model_dump()

with st.form("profile_form"):
    c1, c2 = st.columns(2)
    with c1:
        st.html('<p style="color:#9CA3AF;font-size:0.8rem;font-weight:500;margin:0 0 4px;text-transform:uppercase;letter-spacing:0.05em;">Legal Name *</p>')
        legal_name = st.text_input("Legal Name *", value=defaults.get("legal_name", ""), label_visibility="collapsed")
    with c2:
        st.html('<p style="color:#9CA3AF;font-size:0.8rem;font-weight:500;margin:0 0 4px;text-transform:uppercase;letter-spacing:0.05em;">Trade Name</p>')
        trade_name = st.text_input("Trade Name", value=defaults.get("trade_name", "") or "", label_visibility="collapsed")

    c1, c2 = st.columns(2)
    with c1:
        st.html('<p style="color:#9CA3AF;font-size:0.8rem;font-weight:500;margin:0 0 4px;text-transform:uppercase;letter-spacing:0.05em;">GSTIN *</p>')
        gstin = st.text_input("GSTIN *", value=defaults.get("gstin", ""), help="15-character GST Identification Number", label_visibility="collapsed")
    with c2:
        st.html('<p style="color:#9CA3AF;font-size:0.8rem;font-weight:500;margin:0 0 4px;text-transform:uppercase;letter-spacing:0.05em;">PAN *</p>')
        pan = st.text_input("PAN *", value=defaults.get("pan", ""), help="10-character Permanent Account Number", label_visibility="collapsed")

    c1, c2 = st.columns(2)
    with c1:
        st.html('<p style="color:#9CA3AF;font-size:0.8rem;font-weight:500;margin:0 0 4px;text-transform:uppercase;letter-spacing:0.05em;">TAN *</p>')
        tan = st.text_input("TAN *", value=defaults.get("tan", ""), help="10-character Tax Deduction Account Number", label_visibility="collapsed")
    with c2:
        st.html('<p style="color:#9CA3AF;font-size:0.8rem;font-weight:500;margin:0 0 4px;text-transform:uppercase;letter-spacing:0.05em;">CIN</p>')
        cin = st.text_input("CIN", value=defaults.get("cin", "") or "", help="21-character Corporate Identity Number", label_visibility="collapsed")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.html('<p style="color:#9CA3AF;font-size:0.8rem;font-weight:500;margin:0 0 4px;text-transform:uppercase;letter-spacing:0.05em;">Street</p>')
        street = st.text_input("Street", value=defaults.get("street", ""), label_visibility="collapsed")
    with c2:
        st.html('<p style="color:#9CA3AF;font-size:0.8rem;font-weight:500;margin:0 0 4px;text-transform:uppercase;letter-spacing:0.05em;">City</p>')
        city = st.text_input("City", value=defaults.get("city", ""), label_visibility="collapsed")
    with c3:
        st.html('<p style="color:#9CA3AF;font-size:0.8rem;font-weight:500;margin:0 0 4px;text-transform:uppercase;letter-spacing:0.05em;">State</p>')
        state = st.text_input("State", value=defaults.get("state", ""), label_visibility="collapsed")
    with c4:
        st.html('<p style="color:#9CA3AF;font-size:0.8rem;font-weight:500;margin:0 0 4px;text-transform:uppercase;letter-spacing:0.05em;">Pincode</p>')
        pincode = st.text_input("Pincode", value=defaults.get("pincode", ""), label_visibility="collapsed")

    c1, c2 = st.columns(2)
    with c1:
        st.html('<p style="color:#9CA3AF;font-size:0.8rem;font-weight:500;margin:0 0 4px;text-transform:uppercase;letter-spacing:0.05em;">Bank Account Number</p>')
        bank_account_number = st.text_input("Bank Account Number", value=defaults.get("bank_account_number", ""), label_visibility="collapsed")
    with c2:
        st.html('<p style="color:#9CA3AF;font-size:0.8rem;font-weight:500;margin:0 0 4px;text-transform:uppercase;letter-spacing:0.05em;">IFSC Code</p>')
        ifsc_code = st.text_input("IFSC Code", value=defaults.get("ifsc_code", ""), help="11-character IFSC", label_visibility="collapsed")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.html('<p style="color:#9CA3AF;font-size:0.8rem;font-weight:500;margin:0 0 4px;text-transform:uppercase;letter-spacing:0.05em;">Contact Name</p>')
        contact_name = st.text_input("Contact Name", value=defaults.get("contact_name", ""), label_visibility="collapsed")
    with c2:
        st.html('<p style="color:#9CA3AF;font-size:0.8rem;font-weight:500;margin:0 0 4px;text-transform:uppercase;letter-spacing:0.05em;">Contact Email</p>')
        contact_email = st.text_input("Contact Email", value=defaults.get("contact_email", ""), label_visibility="collapsed")
    with c3:
        st.html('<p style="color:#9CA3AF;font-size:0.8rem;font-weight:500;margin:0 0 4px;text-transform:uppercase;letter-spacing:0.05em;">Contact Phone</p>')
        contact_phone = st.text_input("Contact Phone", value=defaults.get("contact_phone", ""), label_visibility="collapsed")

    st.html('<p style="color:#9CA3AF;font-size:0.8rem;font-weight:500;margin:0 0 4px;text-transform:uppercase;letter-spacing:0.05em;">Contact Designation</p>')
    contact_designation = st.text_input("Contact Designation", value=defaults.get("contact_designation", "") or "", label_visibility="collapsed")

    submitted = st.form_submit_button("Save Profile")

if submitted:
    try:
        new_profile = CompanyProfile(
            legal_name=legal_name, trade_name=trade_name or None, gstin=gstin, pan=pan, tan=tan,
            cin=cin or None, street=street, city=city, state=state, pincode=pincode,
            bank_account_number=bank_account_number, ifsc_code=ifsc_code,
            contact_name=contact_name, contact_email=contact_email, contact_phone=contact_phone,
            contact_designation=contact_designation or None,
        )
        save_profile(new_profile, "data/profile.json")
        st.session_state["profile"] = new_profile
        st.success("Profile saved successfully!")
    except ValidationError as e:
        st.error(f"Validation error: {e}")

st.divider()

# ── SECTION 2 — Document Vault ──
st.html(section_header("Document Vault", badge="Required"))

doc_types = list(DocumentType)
cols = st.columns(2)

for i, doc_type in enumerate(doc_types):
    with cols[i % 2]:
        existing = vault.get_document(doc_type)
        st.html(f"""
        <div style="background:rgba(22, 27, 34, 0.95);border:1px solid #30363D;border-radius:8px;padding:1.25rem;margin-bottom:1rem;">
            <div style="display:flex;align-items:center;
                 justify-content:space-between;
                 margin-bottom:0.5rem;">
                <span style="color:#C9D1D9;font-weight:500;
                      font-size:0.875rem;">
                      {doc_type.value.replace('_', ' ').title()}
                </span>
                <span style="color:#8B949E;font-size:0.75rem;
                      text-transform:uppercase;
                      letter-spacing:0.05em;">
                      Required
                </span>
            </div>
        """)
        if existing:
            st.html('<span style="color:#3FB950;font-size:0.85rem;font-weight:500;">✓ Uploaded</span>')
        else:
            st.html('<span style="color:#8B949E;font-size:0.85rem;">Not uploaded</span>')

        uploaded = st.file_uploader(f"Upload {doc_type.value}", type=["pdf", "jpg", "jpeg", "png"],
                                     key=f"upload_{doc_type.value}", label_visibility="collapsed")
        if uploaded is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded.name)[1]) as tmp:
                tmp.write(uploaded.getbuffer())
                tmp_path = tmp.name
            try:
                vault.add_document(doc_type, tmp_path)
                st.success(f"{doc_type.value} uploaded!")
                st.rerun()
            except ValueError as e:
                st.error(str(e))
            finally:
                os.unlink(tmp_path)
        st.html("</div>")

st.divider()

# ── SECTION 3 — Preflight Check ──
st.html(section_header("Preflight Check"))

if st.button("Run Preflight Check", type="primary"):
    current_profile = st.session_state.get("profile")
    if not current_profile:
        st.warning("Save your profile first.")
    else:
        report = run_preflight(current_profile, vault)
        st.session_state["preflight_report"] = report
        if report.is_ready:
            st.html("""
            <div style="display:inline-block;background:rgba(63,185,80,0.1);
                  color:#3FB950;font-size:0.875rem;
                  font-weight:600;padding:6px 16px;
                  border-radius:50px;
                  border:1px solid rgba(63,185,80,0.2);margin-bottom:1rem;">
                  All checks passed — Ready to run!
            </div>
            """)
        else:
            st.html("""
            <div style="display:inline-block;background:rgba(248,81,73,0.1);
                  color:#F85149;font-size:0.875rem;
                  font-weight:600;padding:6px 16px;
                  border-radius:50px;
                  border:1px solid rgba(248,81,73,0.2);margin-bottom:1rem;">
                  Fix Error items before running
            </div>
            """)
        for item in report.items:
            if item.status == "GREEN":
                st.success(f"Passed: {item.check_name} — {item.message}")
            elif item.status == "YELLOW":
                st.warning(f"Warning: {item.check_name} — {item.message}")
            else:
                st.error(f"Failed: {item.check_name} — {item.message}")
