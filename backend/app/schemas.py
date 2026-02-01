from pydantic import BaseModel
from typing import List, Optional

class FileResponse(BaseModel):
    filename: str
    size: float 
    hash: str
    status: str
    uploaded_at: str
    reason: Optional[str] = None

class PolicyUpdateRequest(BaseModel):
    max_file_size: Optional[int] = None
    allowed_mime_types: Optional[List[str]] = None
    hash_blacklist: Optional[List[str]] = None
    filename_pattern: Optional[str] = None

