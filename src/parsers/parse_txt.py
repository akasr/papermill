from src.parsers.utils import normalize_line_endings
from fastapi import HTTPException

# Constants
BINARY_CHECK_SAMPLE_SIZE = 8192  # 8KB
BINARY_THRESHOLD = 0.3  # 30% non-text characters


def is_binary(file: bytes) -> bool:
    """
    Detect if a file is binary by checking for null bytes and
    the ratio of non-text characters.
    """
    # Check for null bytes (common in binary files)
    if b"\x00" in file[:BINARY_CHECK_SAMPLE_SIZE]:
        return True

    # Sample the file (check first 8KB or entire file if smaller)
    sample = file[:BINARY_CHECK_SAMPLE_SIZE]

    # Count non-text bytes (control characters except whitespace)
    non_text_chars = 0
    for byte in sample:
        # Allow common text characters: printable ASCII, tabs, newlines, carriage returns
        if byte < 32 and byte not in (9, 10, 13):  # Tab, LF, CR
            non_text_chars += 1
        elif byte == 127:  # DEL character
            non_text_chars += 1

    # If more than 30% non-text characters, consider it binary
    if len(sample) > 0 and (non_text_chars / len(sample)) > BINARY_THRESHOLD:
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
