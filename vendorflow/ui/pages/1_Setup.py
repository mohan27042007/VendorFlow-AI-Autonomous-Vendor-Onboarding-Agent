"""Setup page — profile input + document upload + preflight."""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from pydantic import ValidationError

from core.document_vault import DocumentType, DocumentVault
from core.preflight import run_preflight
from core.profile import CompanyProfile, load_profile, save_profile

st.header("⚙️ Setup")

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

# ──────────────────────────────────────────────
# SECTION 1 — Company Profile
# ──────────────────────────────────────────────
st.subheader("Company Profile")

defaults = {}
if profile:
    defaults = profile.model_dump()

with st.form("profile_form"):
    c1, c2 = st.columns(2)
    with c1:
        legal_name = st.text_input("Legal Name *", value=defaults.get("legal_name", ""))
    with c2:
        trade_name = st.text_input("Trade Name", value=defaults.get("trade_name", "") or "")

    c1, c2 = st.columns(2)
    with c1:
        gstin = st.text_input("GSTIN *", value=defaults.get("gstin", ""), help="15-character GST Identification Number")
    with c2:
        pan = st.text_input("PAN *", value=defaults.get("pan", ""), help="10-character Permanent Account Number")

    c1, c2 = st.columns(2)
    with c1:
        tan = st.text_input("TAN *", value=defaults.get("tan", ""), help="10-character Tax Deduction Account Number")
    with c2:
        cin = st.text_input("CIN", value=defaults.get("cin", "") or "", help="21-character Corporate Identity Number")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        street = st.text_input("Street", value=defaults.get("street", ""))
    with c2:
        city = st.text_input("City", value=defaults.get("city", ""))
    with c3:
        state = st.text_input("State", value=defaults.get("state", ""))
    with c4:
        pincode = st.text_input("Pincode", value=defaults.get("pincode", ""))

    c1, c2 = st.columns(2)
    with c1:
        bank_account_number = st.text_input("Bank Account Number", value=defaults.get("bank_account_number", ""))
    with c2:
        ifsc_code = st.text_input("IFSC Code", value=defaults.get("ifsc_code", ""), help="11-character IFSC")

    c1, c2, c3 = st.columns(3)
    with c1:
        contact_name = st.text_input("Contact Name", value=defaults.get("contact_name", ""))
    with c2:
        contact_email = st.text_input("Contact Email", value=defaults.get("contact_email", ""))
    with c3:
        contact_phone = st.text_input("Contact Phone", value=defaults.get("contact_phone", ""))

    contact_designation = st.text_input("Contact Designation", value=defaults.get("contact_designation", "") or "")

    submitted = st.form_submit_button("Save Profile")

if submitted:
    try:
        new_profile = CompanyProfile(
            legal_name=legal_name,
            trade_name=trade_name or None,
            gstin=gstin,
            pan=pan,
            tan=tan,
            cin=cin or None,
            street=street,
            city=city,
            state=state,
            pincode=pincode,
            bank_account_number=bank_account_number,
            ifsc_code=ifsc_code,
            contact_name=contact_name,
            contact_email=contact_email,
            contact_phone=contact_phone,
            contact_designation=contact_designation or None,
        )
        save_profile(new_profile, "data/profile.json")
        st.session_state["profile"] = new_profile
        st.success("Profile saved successfully!")
    except ValidationError as e:
        st.error(f"Validation error: {e}")

st.divider()

# ──────────────────────────────────────────────
# SECTION 2 — Document Vault
# ──────────────────────────────────────────────
st.subheader("Document Vault")

doc_types = list(DocumentType)
cols = st.columns(2)

for i, doc_type in enumerate(doc_types):
    with cols[i % 2]:
        existing = vault.get_document(doc_type)
        if existing:
            st.markdown(f"✅ **{doc_type.value}** — uploaded")
        else:
            st.markdown(f"⬜ **{doc_type.value}**")

        uploaded = st.file_uploader(
            f"Upload {doc_type.value}",
            type=["pdf", "jpg", "jpeg", "png"],
            key=f"upload_{doc_type.value}",
            label_visibility="collapsed",
        )
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

st.divider()

# ──────────────────────────────────────────────
# SECTION 3 — Preflight Check
# ──────────────────────────────────────────────
st.subheader("Preflight Check")

if st.button("Run Preflight Check"):
    current_profile = st.session_state.get("profile")
    if not current_profile:
        st.warning("Save your profile first.")
    else:
        report = run_preflight(current_profile, vault)
        st.session_state["preflight_report"] = report

        st.markdown(f"**Ready: {'YES' if report.is_ready else 'NO'}**")

        for item in report.items:
            if item.status == "GREEN":
                st.success(f"✅ {item.check_name}: {item.message}")
            elif item.status == "YELLOW":
                st.warning(f"⚠️ {item.check_name}: {item.message}")
            else:
                st.error(f"❌ {item.check_name}: {item.message}")

        if report.is_ready:
            st.success("✅ All checks passed. Ready to run!")
        else:
            st.error("❌ Fix RED items before running.")
