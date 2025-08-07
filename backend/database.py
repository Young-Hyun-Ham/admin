import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()  # ✅ .env 환경변수 로드

# ✅ 환경변수 불러오기
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# ✅ 비동기 PostgreSQL URL 구성
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ✅ 비동기 엔진 생성
engine = create_async_engine(DATABASE_URL, echo=True)

# ✅ 세션 클래스 생성
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# ✅ 모델 선언용 Base 클래스
Base = declarative_base()

# ✅ 의존성 주입용 세션 생성기
async def get_db():
    async with SessionLocal() as session:
        yield session
