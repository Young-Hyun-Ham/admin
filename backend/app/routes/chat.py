# app/routes/chat.py
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import ChatStreamRequest
from ..chat_service import stream_openai_chat
from ..rag_service import search_similar_docs
from ..models import Conversation
from ..database import get_session
import traceback
from utils.jwt import verify_token

router = APIRouter(
    prefix="/chat/stream",
    tags=["chat"],
    dependencies=[Depends(verify_token)] # /chat/stream/** 들어오는 모든 엔드포인트에 JWT 인증 적용
    )

@router.post("/")
async def chat_stream(req: ChatStreamRequest, db: AsyncSession = Depends(get_session)):
    async def event_generator():
        assistant_reply = ""

        try:
            # 1) 유저/시스템 메시지 저장 (커밋은 마지막에 한 번만)
            for m in req.messages:
                db.add(Conversation(role=m.role, content=m.content))

            # 2) 최근 user 질문
            user_question = next((m.content for m in reversed(req.messages) if m.role == "user"), "")

            # 3) RAG 검색
            docs = await search_similar_docs(db, user_question)

            def pick_content(d):
                if hasattr(d, "content"):  # ORM 객체
                    return d.content or ""
                if isinstance(d, dict):
                    return d.get("content", "")
                return str(d)

            context_text = "\n\n".join(pick_content(d) for d in (docs or [])) or "No relevant context found."

            # 4) 시스템 프롬프트 + 원본 메시지(dict로)
            rag_prompt = (
                "You are a helpful assistant. Use the following context to answer the question.\n\n"
                f"Context:\n{context_text}\n\n"
                "Answer in Korean if the question is in Korean."
            )
            all_messages = [{"role": "system", "content": rag_prompt}] + [m.model_dump() for m in req.messages]

            # 5) OpenAI 스트림 → 플레인 텍스트로 그대로 흘리기
            async for chunk in stream_openai_chat(all_messages, getattr(req, "model", None) or "gpt-4o-mini"):
                if not chunk:
                    continue
                if isinstance(chunk, bytes):
                    data = chunk
                else:
                    data = str(chunk).encode("utf-8")
                assistant_reply += data.decode("utf-8", errors="ignore")
                yield data

            # 6) assistant 저장 + 커밋
            db.add(Conversation(role="assistant", content=assistant_reply))
            await db.commit()

        except Exception:
            # ✅ 여기서 예외를 먹고, 에러 메시지를 마지막으로 흘려보낸 뒤 종료
            print("STREAM ERROR:\n", traceback.format_exc())
            err_text = "\n\n[stream-error] backend exception occurred. See server logs."
            yield err_text.encode("utf-8")

    # 플레인 텍스트 스트림
    return StreamingResponse(event_generator(), media_type="text/plain; charset=utf-8")
