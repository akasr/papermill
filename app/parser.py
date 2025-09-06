import pymupdf
import re

def clean_text(text: str) -> str:
    """Clean and normalize extracted text.

    Args:
        text (str): The raw text extracted from the document.

    Returns:
        str: The cleaned and normalized text.
    """
    text = re.sub(r'(\r?\n){3,}', '\n\n', text).strip()
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()

def parse_pdf(file_path: str) -> dict:
    """Parse a PDF file and extract its text content.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        dict: A dictionary with page numbers as keys and extracted text as values.
    """
    document = pymupdf.open(file_path)
    parsed_content = {"pages": []}

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = clean_text(page.get_text())
        parsed_content["pages"].append({"number": page_num + 1, "text": text})

    return parsed_content