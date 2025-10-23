from io import BytesIO
from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_extract_from_url():
    url = "https://pdfobject.com/pdf/sample.pdf"
    response = client.post("/extract/url", json={"url": url})
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert "metadata" in data


def test_extract_txt_file():
    """Test uploading a text file."""
    with open("tests/sample_files/sample.txt", "rb") as f:
        response = client.post(
            "/extract",
            files={"file": ("sample.txt", f, "text/plain")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert len(data["text"]) > 0
    assert data["metadata"]["filename"] == "sample.txt"
    assert data["metadata"]["content_type"] == "text/plain"
    assert data["metadata"]["line_count"] is not None
    assert data["metadata"]["word_count"] is not None
    assert data["metadata"]["char_count"] is not None


def test_extract_pdf_file():
    """Test uploading a PDF file."""
    with open("tests/sample_files/sample.pdf", "rb") as f:
        response = client.post(
            "/extract",
            files={"file": ("sample.pdf", f, "application/pdf")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert len(data["text"]) > 0
    assert data["metadata"]["filename"] == "sample.pdf"
    assert data["metadata"]["content_type"] == "application/pdf"
    assert data["metadata"]["page_count"] is not None
    assert data["metadata"]["page_count"] > 0


def test_extract_docx_file():
    """Test uploading a DOCX file."""
    with open("tests/sample_files/sample.docx", "rb") as f:
        response = client.post(
            "/extract",
            files={"file": ("sample.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert len(data["text"]) > 0
    assert data["metadata"]["filename"] == "sample.docx"
    assert data["metadata"]["content_type"] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    assert data["metadata"]["word_count"] is not None
    assert data["metadata"]["char_count"] is not None


def test_extract_file_too_large():
    """Test that files exceeding size limit are rejected."""
    # Create a 6MB file (exceeds 5MB limit)
    large_content = b"x" * (6 * 1024 * 1024)
    file = BytesIO(large_content)
    
    response = client.post(
        "/extract",
        files={"file": ("large.txt", file, "text/plain")}
    )
    
    assert response.status_code == 413
    assert "exceeds 5MB" in response.json()["detail"]


def test_extract_empty_file():
    """Test that empty files are rejected."""
    file = BytesIO(b"")
    
    response = client.post(
        "/extract",
        files={"file": ("empty.txt", file, "text/plain")}
    )
    
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_extract_unsupported_file_type():
    """Test that unsupported file types are rejected."""
    file = BytesIO(b"fake image content")
    
    response = client.post(
        "/extract",
        files={"file": ("image.png", file, "image/png")}
    )
    
    assert response.status_code == 415
    assert "Unsupported file type" in response.json()["detail"]