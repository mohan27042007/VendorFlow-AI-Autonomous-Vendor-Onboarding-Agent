"""Company profile manager tests."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from core.profile import CompanyProfile, load_profile, profile_to_dict, save_profile

SAMPLE_PATH = "data/sample_profile.json"


def test_valid_profile_loads():
    """sample_profile.json loads cleanly."""
    profile = load_profile(SAMPLE_PATH)
    assert profile.legal_name == "Acme Solutions Private Limited"
    assert profile.gstin == "27AAPFU0939F1ZV"
    assert profile.pan == "AAPFU0939F"


def test_invalid_gstin_raises():
    """Bad GSTIN raises ValidationError."""
    data = json.loads(Path(SAMPLE_PATH).read_text())
    data["gstin"] = "INVALID_GSTIN_123"
    with pytest.raises(ValidationError, match="GSTIN"):
        CompanyProfile(**data)


def test_invalid_pan_raises():
    """Bad PAN raises ValidationError."""
    data = json.loads(Path(SAMPLE_PATH).read_text())
    data["pan"] = "BADPAN"
    with pytest.raises(ValidationError, match="PAN"):
        CompanyProfile(**data)


def test_missing_file_raises():
    """FileNotFoundError for missing path."""
    with pytest.raises(FileNotFoundError):
        load_profile("data/nonexistent_profile.json")


def test_profile_to_dict_complete():
    """All fields present in output dict."""
    profile = load_profile(SAMPLE_PATH)
    d = profile_to_dict(profile)
    assert "legal_name" in d
    assert "gstin" in d
    assert "pan" in d
    assert "contact_email" in d
    assert "bank_account_number" in d
    assert "ifsc_code" in d
    assert len(d) == 16
