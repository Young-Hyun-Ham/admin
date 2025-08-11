from fastapi import APIRouter, Depends, HTTPException, Response, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Any, Dict
import json

from backend.models.board import Board
from backend.database import get_db

router = APIRouter(
    prefix="/api/board",
    tags=["board"],
    )

@router.get("/")
async def get_board_list(
    response: Response,
    filter: str = Query("{}"),
    range: str = Query("[0,9]"),
    sort: str = Query('["id","ASC"]'),
    db: AsyncSession = Depends(get_db),
):
    # react-admin 쿼리 파라미터 파싱
    f = json.loads(filter)
    r = json.loads(range)
    s = json.loads(sort)

    start = r[0]
    end = r[1]
    limit = end - start + 1

    sort_col = getattr(Board, s[0])
    if s[1].lower() == "desc":
        sort_col = sort_col.desc()

    query = select(Board)

    # 아주 단순한 like 필터(필요 시 확장)
    for k, v in f.items():
        col = getattr(Board, k, None)
        if col is not None and isinstance(v, str):
            query = query.where(col.like(f"%{v}%"))

    # total
    total = (await db.execute(select(Board))).scalars().unique().all()
    total_count = len(total)

    # paging
    rows = (await db.execute(query.order_by(sort_col).offset(start).limit(limit))).scalars().all()

    # react-admin: Content-Range 헤더 필수 + CORS expose 필요
    response.headers["Content-Range"] = f"board {start}-{start + len(rows) - 1}/{total_count}"
    return [row.as_dict() for row in rows]

@router.get("/{id}")
async def get_board_one(id: int, db: AsyncSession = Depends(get_db)):
    row = (await db.execute(select(Board).where(Board.id == id))).scalars().first()
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    return row.as_dict()

@router.post("/")
async def create_board(payload: Dict[str, Any], db: AsyncSession = Depends(get_db)):
    row = Board(title=payload.get("title"), body=payload.get("body"))
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row.as_dict()

@router.put("/{id}")
async def update_board(id: int, payload: Dict[str, Any], db: AsyncSession = Depends(get_db)):
    row = (await db.execute(select(Board).where(Board.id == id))).scalars().first()
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    row.title = payload.get("title", row.title)
    row.body  = payload.get("body", row.body)
    await db.commit()
    await db.refresh(row)
    return row.as_dict()

@router.delete("/{id}")
async def delete_board(id: int, db: AsyncSession = Depends(get_db)):
    row = (await db.execute(select(Board).where(Board.id == id))).scalars().first()
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    await db.delete(row)
    await db.commit()
    return {"id": id}
