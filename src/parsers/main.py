import chardet
import hashlib
from fastapi import UploadFile, HTTPException
from src.custom_types import Metadata, Result
from src.parsers.parse_txt import parse_txt_content
from src.parsers.parse_pdf import parse_pdf_content
from src.parsers.parse_docx import parse_docx_content

# Constants
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes


def detect_encoding(file: bytes) -> tuple[str, float]:
    """Detect the encoding of a byte string using chardet."""
    detected = chardet.detect(file)
    encoding = detected["encoding"] or "utf-8"
    confidence = detected["confidence"] or 0.0

    return encoding, confidence


async def parser(file: UploadFile) -> Result:
    """Parse an uploaded file and extract text and metadata."""
    file_bytes = await file.read()
    size = len(file_bytes)

    if size == 0:
        raise HTTPException(status_code=400, detail="File is empty")
    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File size exceeds 5MB")

    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    encoding, confidence = detect_encoding(file_bytes)
    text = None
    page_count = None

    match file.content_type:
        case "application/pdf":
            text, page_count = parse_pdf_content(file_bytes)
        case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = parse_docx_content(file_bytes)
        case "text/plain":
            text = parse_txt_content(file_bytes, encoding)
        case _:
            raise HTTPException(status_code=415, detail="Unsupported file type")

    lines = text.splitlines()
    words = text.split()
    line_count = len(lines)
    word_count = len(words)
    char_count = len(text)

    metadata = Metadata(
        filename=file.filename,
        content_type=file.content_type,
        encoding=encoding,
        encoding_confidence=confidence,
        size=size,
        sha256=hashlib.sha256(file_bytes).hexdigest(),
        page_count=page_count,
        line_count=line_count,
        word_count=word_count,
        char_count=char_count,
        language=None,
    )

    return Result(text=text, metadata=metadata, summary=None)
