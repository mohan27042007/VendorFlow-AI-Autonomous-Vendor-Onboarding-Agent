"""Preflight compliance scanner tests."""

import pytest
from pydantic import ValidationError

from core.document_vault import DocumentType, DocumentVault
from core.preflight import PreflightReport, run_preflight
from core.profile import CompanyProfile, load_profile


@pytest.fixture
def profile():
    return load_profile("data/sample_profile.json")


@pytest.fixture
def empty_vault(tmp_path):
    return DocumentVault(uploads_dir=str(tmp_path))


def test_all_green_no_docs(profile, empty_vault):
    """Valid profile, empty vault → GST cert check RED, rest GREEN/YELLOW, is_ready=False."""
    report = run_preflight(profile, empty_vault)
    assert report.is_ready is False
    red_items = [i for i in report.items if i.status == "RED"]
    assert any("GST Certificate" in i.check_name for i in red_items)


def test_ready_with_valid_profile(profile, tmp_path):
    """Valid profile + mock vault that returns a path for GST_CERT → is_ready=True."""
    vault = DocumentVault(uploads_dir=str(tmp_path))
    # Create a dummy PDF for GST cert
    import fitz
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), f"GST Certificate for {profile.legal_name}")
    pdf_path = str(tmp_path / "GST_CERT_dummy.pdf")
    doc.save(pdf_path)
    doc.close()
    vault.add_document(DocumentType.GST_CERT, pdf_path)
    report = run_preflight(profile, vault)
    assert report.is_ready is True
    assert report.red_count == 0


def test_invalid_gstin_red(profile, empty_vault):
    """Profile with bad GSTIN → that check is RED."""
    profile.gstin = "INVALID_GSTIN_123"
    report = run_preflight(profile, empty_vault)
    gstin_items = [i for i in report.items if "GSTIN" in i.check_name]
    assert any(i.status == "RED" for i in gstin_items)


def test_missing_required_field_red(profile, empty_vault):
    """Profile with empty legal_name → required fields check RED."""
    profile.legal_name = ""
    report = run_preflight(profile, empty_vault)
    field_items = [i for i in report.items if "Required Fields" in i.check_name]
    assert any(i.status == "RED" for i in field_items)


def test_report_counts_correct(profile, empty_vault):
    """green_count + yellow_count + red_count == total number of checks (8)."""
    report = run_preflight(profile, empty_vault)
    assert report.green_count + report.yellow_count + report.red_count == len(report.items)
    assert len(report.items) == 8
