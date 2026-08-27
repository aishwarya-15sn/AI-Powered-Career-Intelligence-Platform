from pathlib import Path

import pymupdf


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from all pages of a PDF resume.

    Args:
        pdf_path: Path to the resume PDF.

    Returns:
        Combined extracted text from the PDF.
    """

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("The uploaded file must be a PDF.")

    text_parts = []

    with pymupdf.open(path) as document:
        for page in document:
            page_text = page.get_text()

            if page_text:
                text_parts.append(page_text)

    return "\n".join(text_parts).strip()