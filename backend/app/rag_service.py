# backend/app/rag_service.py

from typing import List, Sequence, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text, func, bindparam
from pgvector.sqlalchemy import Vector
from openai import OpenAI
from openai import APIConnectionError, APITimeoutError, APIStatusError  # 에러 타입
from .config import get_settings
from .models import Document

settings = get_settings()
client = OpenAI(api_key=settings.OPENAI_API_KEY)
EMBED_DIM = settings.EMBEDDING_DIM

# ---- embeddings --------------------------------------------------------------
def _embed(text: str) -> Optional[List[float]]:
    """네트워크/권한 에러가 나면 None을 반환해서 상위 로직이 '컨텍스트 없음'으로 진행하도록."""
    try:
        res = client.embeddings.create(model=settings.EMBEDDING_MODEL, input=text)
        return res.data[0].embedding
    except (APIConnectionError, APITimeoutError, APIStatusError, Exception) as e:
        print("[embed error]", type(e).__name__, str(e))
        return None

async def embed_many(texts: Sequence[str]) -> List[List[float]]:
    # 간단히 순차로 _embed 재사용(안정성 우선). 속도 필요하면 배치 호출로 개선.
    return [_embed(t) for t in texts]

# ---- simple CRUD for Document (pgvector 컬럼) ---------------------------------
async def add_document(db: AsyncSession, text: str) -> Document:
    emb = _embed(text)
    doc = Document(content=text, embedding=emb)
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc

async def update_document(db: AsyncSession, doc_id: int, text: str) -> Document | None:
    doc = await db.get(Document, doc_id)
    if not doc:
        return None
    emb = _embed(text)
    doc.content = text
    doc.embedding = emb
    await db.commit()
    await db.refresh(doc)
    return doc

# ---- similarity search (Documents 테이블 기준) --------------------------------
async def search_similar_docs(db: AsyncSession, query: str, top_k: int = 3):
    """
    l2_distance로 유사도 검색. score가 낮을수록 더 유사.
    """
    q_emb = _embed(query)
    emb_param = bindparam("q_emb", value=q_emb, type_=Vector(EMBED_DIM))
    stmt = (
        select(
            Document.id,
            Document.content,
            func.l2_distance(Document.embedding, emb_param).label("score"),
        )
        .order_by("score")
        .limit(top_k)
    )
    rows = (await db.execute(stmt)).all()
    return [{"id": r.id, "content": r.content, "score": float(r.score)} for r in rows]

# ---- similarity search (chunks 테이블 기준; 필요 시 사용) ---------------------
async def vector_search(session: AsyncSession, query: str, k: int = 5):
    q_emb = _embed(query)
    rows = await session.execute(
        text("""
            SELECT id, document_id, chunk_index, content,
                   1 - (embedding <=> :emb) AS score
            FROM chunks
            ORDER BY embedding <=> :emb
            LIMIT :k
        """),
        {"emb": q_emb, "k": k},
    )
    return [dict(r._mapping) for r in rows.fetchall()]

# ---- 텍스트 청킹 유틸 ---------------------------------------------------------
def chunk_text(s: str, target_len: int = 1200, overlap: int = 150) -> List[str]:
    out, start = [], 0
    n = len(s)
    if n == 0:
        return out
    while start < n:
        end = min(n, start + target_len)
        out.append(s[start:end])
        start = max(0, end - overlap)
    return out
