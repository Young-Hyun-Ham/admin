# backend/app/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, computed_field

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
    LANGSMITH_API_KEY: str | None = None

    # 3) RAG
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    CHAT_MODEL: str = "gpt-4o-mini"
    EMBEDDING_DIM: int = 1536

    # 4) Upload
    UPLOAD_DIR: str = "./data/docs"

    # 5) JWT (이미 기존 백엔드에 있을 걸 대비해서 살려둠)
    jwt_secret_key: str | None = None
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    # 6) CORS
    cors_allow_origins: str | None = None  # "http://localhost:5173,http://127.0.0.1:5173"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",   # ✅ .env에 추가 키 있어도 무시
    )

    @computed_field
    @property
    def db_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        if all([self.db_host, self.db_port, self.db_name, self.db_user, self.db_password]):
            return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        # 기본값 (없으면 로컬 디폴트)
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