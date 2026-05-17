from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.models.document import DocumentStatus


class DocumentResponse(BaseModel):

    id: str
    filename: str
    file_type: str
    file_size_bytes: int
    page_count: int
    chunk_count: int
    status: DocumentStatus

    error_message: Optional[str] = None

    uploaded_at: datetime

    processed_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class DocumentListResponse(BaseModel):

    documents: List[DocumentResponse]

    total: int


class QueryRequest(BaseModel):

    query: str

    top_k: int = 5


class SourceChunk(BaseModel):

    text: str

    filename: str

    chunk_index: int

    score: float


class QueryResponse(BaseModel):

    query: str

    answer: str

    sources: List[SourceChunk]


class HealthResponse(BaseModel):

    status: str

    version: str

    llm_provider: str