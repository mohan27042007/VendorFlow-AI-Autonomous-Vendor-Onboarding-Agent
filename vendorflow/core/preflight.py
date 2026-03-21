"""Preflight compliance scanner — F14."""

import re
from dataclasses import dataclass, field

import fitz

from core.document_vault import DocumentType, DocumentVault
from core.profile import CompanyProfile


@dataclass
class PreflightItem:
    check_name: str
    status: str  # "GREEN" | "YELLOW" | "RED"
    message: str


@dataclass
class PreflightReport:
    items: list[PreflightItem] = field(default_factory=list)
    is_ready: bool = False
    green_count: int = 0
    yellow_count: int = 0
    red_count: int = 0


def run_preflight(profile: CompanyProfile, vault: DocumentVault) -> PreflightReport:
    """Run all preflight checks and return a report."""
    items: list[PreflightItem] = []

    # CHECK 1 — GSTIN format
    if re.match(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$", profile.gstin):
        items.append(PreflightItem("GSTIN Format", "GREEN", f"GSTIN format valid: {profile.gstin}"))
    else:
        items.append(PreflightItem("GSTIN Format", "RED", f"GSTIN format invalid: {profile.gstin}"))

    # CHECK 2 — PAN format
    if re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]$", profile.pan):
        items.append(PreflightItem("PAN Format", "GREEN", f"PAN format valid: {profile.pan}"))
    else:
        items.append(PreflightItem("PAN Format", "RED", f"PAN format invalid: {profile.pan}"))

    # CHECK 3 — TAN format
    if re.match(r"^[A-Z]{4}[0-9]{5}[A-Z]$", profile.tan):
        items.append(PreflightItem("TAN Format", "GREEN", f"TAN format valid: {profile.tan}"))
    else:
        items.append(PreflightItem("TAN Format", "RED", f"TAN format invalid: {profile.tan}"))

    # CHECK 4 — Required fields not empty
    required = ["legal_name", "gstin", "pan", "bank_account_number", "ifsc_code", "contact_name", "contact_email"]
    missing = [f for f in required if not getattr(profile, f)]
    if not missing:
        items.append(PreflightItem("Required Fields", "GREEN", "All required fields present"))
    else:
        items.append(PreflightItem("Required Fields", "RED", f"Missing required fields: {', '.join(missing)}"))

    # CHECK 5 — GST certificate uploaded
    if vault.get_document(DocumentType.GST_CERT) is not None:
        items.append(PreflightItem("GST Certificate", "GREEN", "GST certificate uploaded"))
    else:
        items.append(PreflightItem("GST Certificate", "RED", "GST certificate missing — required for most portals"))

    # CHECK 6 — PAN card uploaded
    if vault.get_document(DocumentType.PAN_CARD) is not None:
        items.append(PreflightItem("PAN Card", "GREEN", "PAN card uploaded"))
    else:
        items.append(PreflightItem("PAN Card", "YELLOW", "PAN card not uploaded — recommended for some portals"))

    # CHECK 7 — Name consistency
    gst_path = vault.get_document(DocumentType.GST_CERT)
    if gst_path and gst_path.lower().endswith(".pdf"):
        try:
            doc = fitz.open(gst_path)
            text = ""
            for page in doc:
                text += str(page.get_text())
            doc.close()
            if profile.legal_name.lower() in text.lower().replace("\n", " ").replace("  ", " "):
                items.append(PreflightItem("Name Consistency", "GREEN", "Company name found in GST certificate"))
            else:
                items.append(PreflightItem("Name Consistency", "YELLOW",
                                           "Company name not found in GST certificate — verify document is correct"))
        except Exception:
            items.append(PreflightItem("Name Consistency", "YELLOW",
                                       "Could not read GST certificate — verify document is correct"))
    else:
        items.append(PreflightItem("Name Consistency", "YELLOW",
                                   "GST certificate not available for name verification"))

    # CHECK 8 — Contact email format
    email = profile.contact_email
    if "@" in email and "." in email.split("@")[-1]:
        items.append(PreflightItem("Contact Email", "GREEN", "Contact email format valid"))
    else:
        items.append(PreflightItem("Contact Email", "YELLOW", f"Contact email format looks invalid: {email}"))

    green = sum(1 for i in items if i.status == "GREEN")
    yellow = sum(1 for i in items if i.status == "YELLOW")
    red = sum(1 for i in items if i.status == "RED")

    return PreflightReport(
        items=items,
        is_ready=(red == 0),
        green_count=green,
        yellow_count=yellow,
        red_count=red,
    )
