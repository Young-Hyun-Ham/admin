from . import logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routers.v1 import auth
from dotenv import load_dotenv
from routers.v1 import v1_routers
import os

logger.info("FastAPI 서버 시작됨")

# .env 파일 로드
load_dotenv()

# .env에서 CORS_ORIGINS 불러오기 (쉼표 구분 허용)
origins = os.getenv("CORS_ALLOW_ORIGINS", "")
allow_origins = [origin.strip() for origin in origins.split(",") if origin.strip()]

app = FastAPI()

# ✅ CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,             # 프론트 주소
    allow_credentials=True,
    allow_methods=["*"],                     # OPTIONS 포함 모든 HTTP 메서드 허용
    allow_headers=["*"],                     # 모든 헤더 허용
)

# 🔹 v1 라우터 전부 등록
for router in v1_routers:
    app.include_router(router, prefix="/v1")
