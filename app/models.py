from pydantic import BaseModel
from typing import List

class Page(BaseModel):
    number: int
    text: str

class ParsedPDFResponse(BaseModel):
    pages: List[Page]


class ErrorResponse(BaseModel):
    detail: str
