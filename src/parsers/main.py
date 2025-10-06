import chardet
import hashlib
from fastapi import UploadFile, HTTPException
from src.custom_types import Metadata, Result
from src.parsers.parse_txt import parse_txt_content


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
    if size > (5 * 1024 * 1024):
        raise HTTPException(status_code=413, detail="File size exceeds 5MB")

    encoding, confidence = detect_encoding(file_bytes)
    text = None

    match file.content_type:
        case "application/pdf":
            text = "pdf"
        case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = "docx"
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
        **{
            "filename": file.filename,
            "content_type": file.content_type,
            "encoding": encoding,
            "encoding_confidence": confidence,
            "size": size,
            "sha256": hashlib.sha256(file_bytes).hexdigest(),
            "page_count": None,
            "line_count": line_count,
            "word_count": word_count,
            "char_count": char_count,
            "language": None,
        }
    )

    return Result(**{"text": text, "metadata": metadata, "summary": None})
