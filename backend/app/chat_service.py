# app/chat_service.py
from datetime import datetime, timezone
from openai import AsyncOpenAI
from langsmith import Client
from .config import settings

oai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
ls = Client()  # 키/엔드포인트는 .env에서 자동 인식 (settings도 OK지만 env가 제일 안전)

async def stream_openai_chat(messages, model: str):
    run = None
    assistant_reply = ""

    # 1) LangSmith run 시작 (옵션: 추적 끄면 건너뜀)
    if settings.LS_TRACING_ENABLED and settings.LS_PROJECT:
        try:
            run = ls.create_run(
                name="chat_stream",
                run_type="chain",                 # "llm"|"tool"|"chain" 중 택1
                project_name=settings.LS_PROJECT,
                inputs={"messages": messages},
                start_time=datetime.now(timezone.utc),
            )
        except Exception as e:
            print("LangSmith create_run error:", e)

    # 2) OpenAI 스트리밍
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
                # generator는 str를 넘겨도 되고, 바깥에서 bytes로 인코딩해도 됨
                yield piece

        # 3) 성공 종료 로깅
        if run is not None:
            try:
                ls.update_run(
                    run_id=run.id,
                    outputs={"response": assistant_reply},
                    end_time=datetime.now(timezone.utc),
                )
            except Exception as e:
                print("LangSmith update_run(ok) error:", e)

    except Exception as e:
        # 3') 실패 종료 로깅
        if run is not None:
            try:
                ls.update_run(
                    run_id=run.id,
                    error=str(e),
                    end_time=datetime.now(timezone.utc),
                )
            except Exception as e2:
                print("LangSmith update_run(err) error:", e2)
        raise
