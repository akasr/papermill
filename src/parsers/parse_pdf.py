import pymupdf
from fastapi import HTTPException
from src.utils import normalize_line_endings


def parse_pdf_content(file: bytes) -> tuple[str, int | None]:
    """Parse PDF content using PyMuPDF."""
    try:
        with pymupdf.open(stream=file, filetype="pdf") as doc:
            text = ""
            page_count = doc.page_count
            for page in doc:
                text += page.get_text()
    except (RuntimeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=f"Error parsing PDF: {str(e)}")

    text = normalize_line_endings(text.strip())
    if text == "":
        raise HTTPException(status_code=400, detail="PDF contains no extractable text")

    return text, page_count
