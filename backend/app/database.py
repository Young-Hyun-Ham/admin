# backend/app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from sqlalchemy.orm import declarative_base
from contextlib import asynccontextmanager
from .config import get_settings

settings = get_settings()
engine = create_async_engine(settings.DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

@asynccontextmanager
async def lifespan_db(app):
    # 확장/테이블 준비 (pgvector)
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.execute(text("""
        CREATE TABLE IF NOT EXISTS documents (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            title TEXT NOT NULL,
            source_path TEXT,
            mime_type TEXT,
            size_bytes BIGINT,
            created_at TIMESTAMPTZ DEFAULT now(),
            updated_at TIMESTAMPTZ DEFAULT now()
        )
        """))
        await conn.execute(text(f"""
        CREATE TABLE IF NOT EXISTS chunks (
            id BIGSERIAL PRIMARY KEY,
            document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
            chunk_index INT NOT NULL,
            content TEXT NOT NULL,
            embedding VECTOR({settings.EMBEDDING_DIM}),
            created_at TIMESTAMPTZ DEFAULT now()
        )
        """))
        await conn.execute(text("CREATE INDEX IF NOT EXISTS idx_chunks_doc ON chunks(document_id)"))
        await conn.execute(text("CREATE INDEX IF NOT EXISTS idx_chunks_embedding ON chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)"))
    yield

async def get_session():
    async with SessionLocal() as session:
        yield session
