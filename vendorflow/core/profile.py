"""Company profile schema and manager — F1."""

import json
from pathlib import Path

from pydantic import BaseModel, EmailStr, field_validator


class CompanyProfile(BaseModel):
    # IDENTITY
    legal_name: str
    trade_name: str | None = None

    # ADDRESS
    street: str
    city: str
    state: str
    pincode: str

    # TAX IDs
    gstin: str
    pan: str
    tan: str
    cin: str | None = None

    # BANK
    bank_account_number: str
    ifsc_code: str

    # CONTACT
    contact_name: str
    contact_email: EmailStr
    contact_phone: str
    contact_designation: str | None = None

    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, v: str) -> str:
        if not v.isdigit() or len(v) != 6:
            raise ValueError("pincode must be exactly 6 digits")
        return v

    @field_validator("gstin")
    @classmethod
    def validate_gstin(cls, v: str) -> str:
        import re
        pattern = r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$"
        if not re.match(pattern, v):
            raise ValueError("invalid GSTIN format")
        return v

    @field_validator("pan")
    @classmethod
    def validate_pan(cls, v: str) -> str:
        import re
        if not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]$", v):
            raise ValueError("invalid PAN format")
        return v

    @field_validator("tan")
    @classmethod
    def validate_tan(cls, v: str) -> str:
        import re
        if not re.match(r"^[A-Z]{4}[0-9]{5}[A-Z]$", v):
            raise ValueError("invalid TAN format")
        return v

    @field_validator("ifsc_code")
    @classmethod
    def validate_ifsc(cls, v: str) -> str:
        import re
        if not re.match(r"^[A-Z]{4}0[A-Z0-9]{6}$", v):
            raise ValueError("invalid IFSC format")
        return v

    @field_validator("contact_phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not v.isdigit() or len(v) != 10:
            raise ValueError("contact_phone must be exactly 10 digits")
        return v


def load_profile(json_path: str) -> CompanyProfile:
    """Read a JSON file and return a validated CompanyProfile."""
    path = Path(json_path)
    if not path.exists():
        raise FileNotFoundError(f"Profile file not found: {json_path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    return CompanyProfile(**data)


def save_profile(profile: CompanyProfile, json_path: str) -> None:
    """Save a CompanyProfile as formatted JSON."""
    path = Path(json_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(profile.model_dump_json(indent=2), encoding="utf-8")


def profile_to_dict(profile: CompanyProfile) -> dict:
    """Return all fields as a flat dict for TinyFish context_data."""
    return profile.model_dump()
