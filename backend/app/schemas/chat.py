from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class ChatRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=20)


class Citation(BaseModel):
    doc_id: str
    chunk_id: str
    page: Optional[int] = None
    text: str


class TraceStep(BaseModel):
    step: str
    tool_name: str
    input: Dict[str, Any]
    output: Dict[str, Any]


class ChatResponse(BaseModel):
    query: str
    answer: str
    citations: List[Citation]
    trace: List[TraceStep]