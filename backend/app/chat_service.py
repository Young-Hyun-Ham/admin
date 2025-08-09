from openai import OpenAI
from langsmith import Client
from .config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)
ls_client = Client(api_key=settings.LANGSMITH_API_KEY)

async def stream_openai_chat(messages: list[dict], model: str):
    """
    OpenAI ChatCompletion을 스트리밍으로 호출
    """
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )
    # for chunk in stream:
    #     delta = chunk.choices[0].delta
    #     if delta and delta.content:
    #         yield delta.content
    async for event in stream:
        delta = getattr(event.choices[0].delta, "content", None)
        if delta:
            yield delta  # str

def log_to_langsmith(messages: list[dict], response: str):
    """ 
    LangSmith에 대화 로그 저장
    """
    try:
        ls_client.create_run(
            project_name=settings.LANGSMITH_PROJECT,
            inputs={"messages": messages},
            outputs={"response": response}
        )
    except Exception as e:
        print("LangSmith logging error:", e)
