from pydantic import BaseModel
from typing import List


class UploadResponse(BaseModel):
    doc_id: str
    filename: str
    saved_path: str
    message: str