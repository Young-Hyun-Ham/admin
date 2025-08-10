from sqlalchemy import Column, BigInteger, DateTime, Integer, String, Text, TIMESTAMP, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .database import Base
from pgvector.sqlalchemy import Vector

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Document(Base):
    __tablename__ = "documents"
    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    source_path = Column(Text)
    mime_type = Column(Text)
    size_bytes = Column(BigInteger)
    embedding = Column(Vector(1536))  # pgvector 임베딩 컬럼 추가
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    chunks = relationship("Chunk", backref="document", cascade="all, delete-orphan")

class Chunk(Base):
    __tablename__ = "chunks"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    # embedding은 raw SQL로 INSERT 시 넣거나 sqlalchemy-vector 패키지 사용 가능
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
