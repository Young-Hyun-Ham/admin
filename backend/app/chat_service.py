# app/chat_service.py
from openai import AsyncOpenAI
from langsmith import traceable
from .config import settings
import asyncio, traceback

oai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

# 프로젝트에 기록하고 싶으면 project_name을 지정
@traceable(name="chat_stream", run_type="chain", project_name=getattr(settings, "LS_PROJECT", None))
async def stream_openai_chat(messages, model: str):
    assistant_reply = ""
    try:
        resp = await oai.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            temperature=0.2,
        )
        async for chunk in resp:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                piece = delta.content
                assistant_reply += piece
                yield piece

    except asyncio.CancelledError:
        # 클라이언트가 스트림을 끊은 경우 — 상위에서 정상 취소 처리
        raise
    except Exception:
        print("STREAM ERROR:\n", traceback.format_exc())
        raise
