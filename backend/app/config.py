# backend/app/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, computed_field
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent   # backend/
ENV_PATH = BASE_DIR / ".env"                        # backend/.env

class Settings(BaseSettings):
    # 1) DB: URL 직접 or 조합형(아래 5개로 조합)
    DATABASE_URL: str | None = Field(default=None)
    db_host: str | None = None
    db_port: int | None = None
    db_name: str | None = None
    db_user: str | None = None
    db_password: str | None = None

    # 2) OpenAI
    OPENAI_API_KEY: str | None = None

    # 3) LangSmith / LangChain (양쪽 이름 모두 허용)
    LANGSMITH_PROJECT: str | None = None
    LANGSMITH_API_KEY: str | None = None
    LANGSMITH_ENDPOINT: str | None = None
    LANGSMITH_TRACING: bool | None = None

    LANGCHAIN_PROJECT: str | None = None
    LANGCHAIN_API_KEY: str | None = None
    LANGCHAIN_ENDPOINT: str | None = None
    LANGCHAIN_TRACING_V2: bool | None = None

    # 4) RAG
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    CHAT_MODEL: str = "gpt-4o-mini"
    EMBEDDING_DIM: int = 1536  # small=1536, large=3072

    # 5) Upload
    UPLOAD_DIR: str = "./data/docs"

    # 6) JWT
    jwt_secret_key: str | None = None
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    # 7) CORS
    cors_allow_origins: str | None = None  # "http://localhost:5173,http://127.0.0.1:5173"

    # ---- Fallback 편의 프로퍼티 (코드는 이걸 쓰면 안전) -------------------------
    @property
    def LS_PROJECT(self) -> str | None:
        return self.LANGSMITH_PROJECT or self.LANGCHAIN_PROJECT

    @property
    def LS_API_KEY(self) -> str | None:
        return self.LANGSMITH_API_KEY or self.LANGCHAIN_API_KEY

    @property
    def LS_ENDPOINT(self) -> str:
        return (self.LANGSMITH_ENDPOINT
                or self.LANGCHAIN_ENDPOINT
                or "https://api.smith.langchain.com")

    @property
    def LS_TRACING_ENABLED(self) -> bool:
        # 둘 중 하나라도 true면 켜진 것으로 판단
        return bool(self.LANGSMITH_TRACING or self.LANGCHAIN_TRACING_V2)

    # -------------------------------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        case_sensitive=False,  # .env 대소문자 상관없이 매핑
        extra="ignore",        # 정의 안 된 env 키는 무시
    )

    @computed_field
    @property
    def db_url(self) -> str:
        """DATABASE_URL이 없을 때 조합형으로 생성."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        if all([self.db_host, self.db_port, self.db_name, self.db_user, self.db_password]):
            return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        # 기본값 (로컬)
        return "postgresql+asyncpg://postgres:1234@localhost:5432/postgres"

    @computed_field
    @property
    def cors_origins_list(self) -> list[str]:
        if not self.cors_allow_origins:
            return ["*"]
        parts = [p.strip() for p in self.cors_allow_origins.split(",") if p.strip()]
        return parts or ["*"]

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
