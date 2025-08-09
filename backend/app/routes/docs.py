# backend/app/routes/docs.py
import os, uuid
from fastapi import APIRouter, UploadFile, File, Form, Depends, BackgroundTasks, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from ..database import get_session
from ..config import get_settings
from ..rag_service import chunk_text, embed_many
from ..schemas import DocumentOut, ChunkOut

router = APIRouter(prefix="/v1/documents", tags=["documents"])
settings = get_settings()

@router.get("", response_model=list[DocumentOut])
async def list_documents(session: AsyncSession = Depends(get_session)):
    rows = await session.execute(text("SELECT * FROM documents ORDER BY created_at DESC"))
    return [dict(r._mapping) for r in rows.fetchall()]

@router.get("/{doc_id}", response_model=DocumentOut)
async def get_document(doc_id: str, session: AsyncSession = Depends(get_session)):
    row = await session.execute(text("SELECT * FROM documents WHERE id = :id::uuid"), {"id": doc_id})
    rec = row.mappings().first()
    if not rec:
        raise HTTPException(status_code=404, detail="Document not found")
    return dict(rec)

@router.delete("/{doc_id}")
async def delete_document(doc_id: str, session: AsyncSession = Depends(get_session)):
    await session.execute(text("DELETE FROM documents WHERE id = :id::uuid"), {"id": doc_id})
    await session.commit()
    return {"ok": True, "id": doc_id}

@router.get("/chunks", response_model=list[ChunkOut])
async def list_chunks(document_id: str = Query(...), session: AsyncSession = Depends(get_session)):
    rows = await session.execute(
        text("""
            SELECT id, document_id, chunk_index, content, NULL::float AS score
            FROM chunks WHERE document_id = :doc::uuid ORDER BY chunk_index
        """),
        {"doc": document_id},
    )
    return [dict(r._mapping) for r in rows.fetchall()]

@router.post("/upload")
async def upload_document(
    background: BackgroundTasks,
    title: str = Form(...),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_id = str(uuid.uuid4())
    dest = os.path.join(settings.UPLOAD_DIR, f"{file_id}__{file.filename}")

    raw = await file.read()
    with open(dest, "wb") as f:
        f.write(raw)

    # documents insert
    row = await session.execute(
        text("""
        INSERT INTO documents(id, title, source_path, mime_type, size_bytes)
        VALUES (:id::uuid, :title, :path, :mime, :size)
        RETURNING id
        """),
        {"id": file_id, "title": title, "path": dest, "mime": file.content_type, "size": len(raw)},
    )
    doc_id = row.scalar_one()
    await session.commit()

    # ingest background: chunk → embed → insert
    async def ingest():
        try:
            text_body = raw.decode(errors="ignore")
            parts = chunk_text(text_body)
            if not parts:
                return
            embs = await embed_many(parts)
            for idx, (p, e) in enumerate(zip(parts, embs)):
                await session.execute(
                    text("""
                    INSERT INTO chunks(document_id, chunk_index, content, embedding)
                    VALUES (:doc::uuid, :idx, :content, :emb)
                    """),
                    {"doc": str(doc_id), "idx": idx, "content": p, "emb": e},
                )
            await session.commit()
        except Exception as e:
            # 실패 로깅만 하고 조용히 종료
            print("[ingest error]", e)

    background.add_task(ingest)
    return {"id": str(doc_id), "title": title}
