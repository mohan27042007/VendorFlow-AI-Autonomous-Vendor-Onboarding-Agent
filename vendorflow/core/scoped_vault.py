"""Scoped data vaults per portal — minimum necessary data — F18."""

from core.blueprint import extract_domain
from core.document_vault import DocumentType, DocumentVault
from core.profile import CompanyProfile, profile_to_dict

PORTAL_DATA_SCOPES = {
    "marketplace": [
        "legal_name", "trade_name", "gstin", "pan",
        "bank_account_number", "ifsc_code",
        "contact_name", "contact_email", "contact_phone",
        "street", "city", "state", "pincode",
    ],
    "government": [
        "legal_name", "trade_name", "gstin", "pan", "tan", "cin",
        "bank_account_number", "ifsc_code",
        "contact_name", "contact_email", "contact_phone",
        "street", "city", "state", "pincode",
    ],
    "default": [
        "legal_name", "gstin", "pan",
        "bank_account_number", "ifsc_code",
        "contact_name", "contact_email", "contact_phone",
    ],
}

PORTAL_CATEGORIES = {
    "indiamart": "marketplace",
    "tradeindia": "marketplace",
    "flipkart": "marketplace",
    "amazon": "marketplace",
    "gem.gov": "government",
    "mkp.gem": "government",
}


def get_portal_category(domain: str) -> str:
    """Return portal category based on domain matching."""
    domain_lower = domain.lower()
    for keyword, category in PORTAL_CATEGORIES.items():
        if keyword in domain_lower:
            return category
    return "default"


def get_scoped_data(portal_url: str, profile: CompanyProfile, vault: DocumentVault) -> dict:
    """Return minimum necessary data for the given portal."""
    domain = extract_domain(portal_url)
    category = get_portal_category(domain)
    fields = PORTAL_DATA_SCOPES[category]

    full_dict = profile_to_dict(profile)
    scoped = {k: full_dict[k] for k in fields if k in full_dict}
    scoped["available_documents"] = list(vault.list_documents().keys())

    return scoped
