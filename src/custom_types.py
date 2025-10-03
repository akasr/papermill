from pydantic import BaseModel


class Metadata(BaseModel):
    filename: str
    content_type: str
    encoding: str
    encoding_confidence: float
    size: int
    sha256: str
    page_count: int | None
    line_count: int | None
    word_count: int | None
    char_count: int | None
    language: str | None


class Result(BaseModel):
    text: str
    metadata: Metadata
    summary: str | None
