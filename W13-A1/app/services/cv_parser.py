"""Helpers for extracting plain text from uploaded CV files."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path


MAX_CV_CHARS = 80_000


def extract_text_from_file(filename: str, content: bytes) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix in {".txt", ".md"}:
        text = content.decode("utf-8", errors="replace")
    elif suffix == ".docx":
        text = _extract_docx(content)
    elif suffix == ".pdf":
        text = _extract_pdf(content)
    else:
        raise ValueError("Unsupported file type. Upload .txt, .md, .docx, or .pdf.")

    text = text.strip()
    if not text:
        raise ValueError("No readable text was found in the uploaded file.")
    return text[:MAX_CV_CHARS]


def _extract_docx(content: bytes) -> str:
    from docx import Document

    document = Document(BytesIO(content))
    paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs]
    return "\n".join(paragraph for paragraph in paragraphs if paragraph)


def _extract_pdf(content: bytes) -> str:
    from pypdf import PdfReader

    reader = PdfReader(BytesIO(content))
    page_text = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(page_text)

