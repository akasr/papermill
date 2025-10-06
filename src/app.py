from fastapi import FastAPI, UploadFile
from src.parsers.main import parser
from src.custom_types import Result

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/extract")
async def extract(file: UploadFile) -> Result:
    result = await parser(file)
    return result
