from pydantic import BaseModel, Field
from typing import List, Optional


class SearchRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=20)


class SearchHit(BaseModel):
    doc_id: str
    chunk_id: str
    text: str
    score: float
    page: Optional[int] = None


class SearchResponse(BaseModel):
    query: str
    hits: List[SearchHit]