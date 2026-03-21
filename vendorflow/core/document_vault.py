"""Document vault — upload once, use everywhere — F2."""

import base64
import shutil
from enum import Enum
from pathlib import Path

import fitz

from config.settings import UPLOADS_DIR

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}


class DocumentType(str, Enum):
    GST_CERT = "GST_CERT"
    PAN_CARD = "PAN_CARD"
    TAN_CERT = "TAN_CERT"
    INCORPORATION_CERT = "INCORPORATION_CERT"
    CANCELLED_CHEQUE = "CANCELLED_CHEQUE"
    MSME_CERT = "MSME_CERT"
    FINANCIALS = "FINANCIALS"


class DocumentVault:
    def __init__(self, uploads_dir: str | None = None):
        self.uploads_dir = Path(uploads_dir or UPLOADS_DIR)
        self.uploads_dir.mkdir(parents=True, exist_ok=True)

    def validate_document(self, file_path: str) -> list[str]:
        """Return list of validation errors (empty = valid)."""
        errors: list[str] = []
        path = Path(file_path)

        if not path.exists():
            errors.append(f"File not found: {file_path}")
            return errors

        if path.suffix.lower() not in ALLOWED_EXTENSIONS:
            errors.append(
                f"Invalid extension '{path.suffix}'. Allowed: {ALLOWED_EXTENSIONS}"
            )

        if path.stat().st_size > MAX_FILE_SIZE:
            errors.append(
                f"File too large: {path.stat().st_size} bytes (max {MAX_FILE_SIZE})"
            )

        if path.suffix.lower() == ".pdf":
            try:
                doc = fitz.open(str(path))
                doc.close()
            except Exception as exc:
                errors.append(f"PDF unreadable: {exc}")

        return errors

    def add_document(self, doc_type: DocumentType, file_path: str) -> str:
        """Copy file to uploads dir and return stored path."""
        errors = self.validate_document(file_path)
        if errors:
            raise ValueError("; ".join(errors))

        src = Path(file_path)
        dest = self.uploads_dir / f"{doc_type.value}_{src.name}"
        shutil.copy2(str(src), str(dest))
        return str(dest)

    def get_document(self, doc_type: DocumentType) -> str | None:
        """Return file path if doc type exists, None otherwise."""
        pattern = f"{doc_type.value}_*"
        matches = list(self.uploads_dir.glob(pattern))
        if matches:
            return str(matches[0])
        return None

    def get_document_as_base64(self, doc_type: DocumentType) -> str | None:
        """Read file and return base64-encoded string."""
        path = self.get_document(doc_type)
        if path is None:
            return None
        return base64.b64encode(Path(path).read_bytes()).decode("utf-8")

    def list_documents(self) -> dict[str, str]:
        """Return {doc_type_value: file_path} for all uploaded docs."""
        docs: dict[str, str] = {}
        for member in DocumentType:
            path = self.get_document(member)
            if path:
                docs[member.value] = path
        return docs
