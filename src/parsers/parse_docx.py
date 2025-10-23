from docx import Document
import io
from fastapi import HTTPException
from src.utils import normalize_line_endings


def parse_docx_content(file: bytes) -> str:
    """Parse DOCX files from bytes."""
    try:
        doc = Document(io.BytesIO(file))
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except (IOError, ValueError) as e:
        raise HTTPException(status_code=400, detail=f"Error parsing DOCX: {e}")

    text = normalize_line_endings(text.strip())
    if text == "":
        raise HTTPException(status_code=400, detail="DOCX contains no extractable text")
    return text
