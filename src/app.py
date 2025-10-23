from fastapi import FastAPI, UploadFile, Body
from src.parsers.main import parser
from src.download import download_file_from_url
from src.custom_types import Result

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/extract")
async def extract(file: UploadFile) -> Result:
    """Extract text and metadata from an uploaded file."""
    result = await parser(file)
    return result

@app.post("/extract/url")
async def extract_from_url(url: str = Body(..., embed=True)) -> Result:
    """Extract text and metadata from a file at a given URL."""
    file = await download_file_from_url(url, timeout=30)
    result = await parser(file)
    return result