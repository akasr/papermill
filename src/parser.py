import chardet
import hashlib
from fastapi import UploadFile, HTTPException
from src.custom_types import Metadata, Result


def detect_encoding(file: bytes) -> tuple[str, float]:
    """Detect the encoding of a byte string using chardet."""
    detected = chardet.detect(file)
    encoding = detected["encoding"] or "utf-8"
    confidence = detected["confidence"] or 0.0

    return encoding, confidence


def normalize_line_endings(text: str) -> str:
    """Normalize all line endings to \n"""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def is_binary(file: bytes) -> bool:
    """
    Detect if a file is binary by checking for null bytes and
    the ratio of non-text characters.
    """
    # Check for null bytes (common in binary files)
    if b"\x00" in file[:8192]:  # Check first 8KB
        return True

    # Sample the file (check first 8KB or entire file if smaller)
    sample = file[:8192]

    # Count non-text bytes (control characters except whitespace)
    non_text_chars = 0
    for byte in sample:
        # Allow common text characters: printable ASCII, tabs, newlines, carriage returns
        if byte < 32 and byte not in (9, 10, 13):  # Tab, LF, CR
            non_text_chars += 1
        elif byte == 127:  # DEL character
            non_text_chars += 1

    # If more than 30% non-text characters, consider it binary
    if len(sample) > 0 and (non_text_chars / len(sample)) > 0.3:
        return True

    return False


def parse_txt_content(file: bytes, encoding: str) -> str:
    """Parse text content, ensuring it's not binary and decoding properly."""
    if is_binary(file):
        raise HTTPException(
            status_code=400, detail="File appears to be binary, not plain text"
        )

    try:
        text = file.decode(encoding)
    except (UnicodeDecodeError, LookupError):
        try:
            text = file.decode("utf-8")
        except UnicodeDecodeError:
            text = file.decode("latin-1")

    text = text.strip()
    text = normalize_line_endings(text)
    # Remove BOM if present
    if text.startswith("\ufeff"):
        text = text[1:]

    if text == "":
        raise HTTPException(status_code=400, detail="File is empty")

    return text


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
