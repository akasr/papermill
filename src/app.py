from fastapi import FastAPI, UploadFile
from src.parser import parser

app = FastAPI()

@app.get('/health')
async def health():
  return {"status": "ok"}

@app.post('/extract')
async def extract(file: UploadFile) -> dict:
  return {
    "filename": file.filename,
    "content_type": file.content_type,
    "size": f"{file.size // 1024} KB" if file.size is not None else "Unknown size",
    "content": await parser(file)
  }