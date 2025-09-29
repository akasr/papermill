from fastapi import UploadFile
import chardet

async def parser(file: UploadFile) -> str:
  content_type = file.content_type
  match content_type:
      case "application/pdf":
          return "pdf"
      case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
          return "docx"
      case "text/plain":
          file_bytes = await file.read()
          
          detected_encoding = chardet.detect(file_bytes)
          encoding = detected_encoding['encoding'] or 'utf-8'

          text = file_bytes.decode(encoding, errors='ignore')
          return text
      case _:
          return content_type or ""