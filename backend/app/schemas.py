# backend/app/schemas.py
from pydantic import BaseModel
from typing import List,  Optional
from uuid import UUID
from datetime import datetime

class DocumentOut(BaseModel):
    id: UUID
    title: str
    source_path: Optional[str] = None
    mime_type: Optional[str] = None
    size_bytes: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ChunkOut(BaseModel):
    id: int
    document_id: UUID
    chunk_index: int
    content: str
    score: Optional[float] = None

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatStreamRequest(BaseModel):
    messages: List[ChatMessage]
    top_k: int = 5  # 옵션

class ChatResponse(BaseModel):
    answer: str
    contexts: List[ChunkOut]
