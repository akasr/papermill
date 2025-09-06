from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
  return {"message": "Hello PaperMill"}

from app.models import ErrorResponse, ParsedPDFResponse
from fastapi import File, UploadFile, HTTPException
@app.post(
  "/parse-pdf/", 
  response_model=ParsedPDFResponse, 
  responses={400: {"model": ErrorResponse}}
)
async def parse_pdf_endpoint(file: UploadFile = File(...)):
  import tempfile
  from app.parser import parse_pdf

  if not file.filename.endswith(".pdf"):
    raise HTTPException(status_code=400, detail="Only PDF files are supported")

  try:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
      contents = await file.read()

      if not contents:
        raise HTTPException(status_code=400, detail="Empty file uploaded")

      tmp.write(contents)
      tmp_path = tmp.name
    file_path = tmp_path

    parsed_content = parse_pdf(file_path)
    return parsed_content
  
  except Exception as e:
    raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {str(e)}")