def normalize_line_endings(text: str) -> str:
    """Normalize all line endings to \n"""
    return text.replace("\r\n", "\n").replace("\r", "\n")
