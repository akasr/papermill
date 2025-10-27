# Papermill
A general-purpose FastAPI microservice that extracts text, structured data from tables, and metadata from various document types (TXT, DOCX, PDF, etc.).

## Core Functions:

- **Document Parsing**: Handles multiple file types (TXT, DOCX and PDF).

- **Metadata Extraction**: Pulls out standard metadata like author, creation date, etc.

- **Output**: Returns a comprehensive JSON object containing all the extracted information.

## Installation and Setup

```bash
# Fork and clone the repository
git clone https://github.com/<username>/papermill.git
cd papermill

# Create a branch for your changes
git checkout -b feature/your-feature-name

# Create and activate a virtual environment
uv venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`

# Install dependencies
uv pip sync requirements.txt

# Start the FastAPI Server
uvicorn src.app:app --reload
```

Push and make a pull request when your changes are ready.

## Endpoints

- `POST /extract`: Upload a document and receive extracted text and metadata.
- `POST /extract/url`: Provide a URL to a document for extraction.
- `GET /health`: Check the health status of the service.
- `GET /docs`: Access the interactive API documentation.