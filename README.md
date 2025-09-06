# PaperMill

PaperMill is a Python-based microservice for document processing. It supports parsing, extracting, and transforming text from multiple document formats ( pdf only for now). Designed to be modular, scalable, and easy to integrate into larger systems.

## Features
- Parse and extract text from PDF documents.

## Setup

```bash
# Clone the repository
git clone https://github.com/akasr/papermill.git
cd papermill

# Create a virtual environment
python -m venv venv
source venv/bin/activate  
# On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload
```

## Usage
Once the server is running, you can access the API at `http://localhost:8000/docs` for the interactive API documentation.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.