# Papermill
A general-purpose FastAPI microservice that extracts text, structured data from tables, and metadata from various document types (TXT, DOCX, PDF, etc.).

## Core Functions:

- **Document Parsing**: Handles multiple file types.

- **Multi-Modal Extraction**: Extracts text from the main body, images (via OCR), and tables.

- **General Summarization**: Generates a concise summary of the document's content without needing a specific user query.

- **Metadata Extraction**: Pulls out standard metadata like author, creation date, etc.

- **Output**: Returns a comprehensive JSON object containing all the extracted information.

## Installation and Setup

```bash
# Clone the repository
git clone https://github.com/akasr/papermill.git
cd papermill

# Create and activate a virtual environment
uv venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`

# Install dependencies
uv pip sync requirements.txt

# Start the FastAPI Server
uvicorn src.app:app --reload
```

## Endpoints

- `POST /extract`: Upload a document and receive extracted text, tables, metadata, and a general summary.
- `GET /health`: Check the health status of the service.
- `GET /docs`: Access the interactive API documentation.