from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pathlib import Path

# .env 로드 (backend/.env를 확실히 찍어서 로드)
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
EXPIRE_MIN = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

# 필수 ENV 확인 (없으면 빨리 터지게)
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY 가 설정되어 있지 않습니다 (.env 확인).")

# Swagger용 토큰 발급 엔드포인트 경로를 실제와 일치
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/api/auth/login")

def create_access_token(subject: str, extra: dict | None = None) -> str:
    """반드시 'sub'에 사용자 식별자(이메일/ID)를 넣어 발급"""
    to_encode = {"sub": str(subject)}
    if extra:
        to_encode.update(extra)

    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MIN)
    to_encode["exp"] = expire

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str = Depends(oauth2_scheme)) -> dict:
    """유효한 토큰이면 payload(일부) 반환, 아니면 401"""
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="유효하지 않은 인증 토큰입니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if not sub:
            raise cred_exc
        # 필요하면 사용자 조회에 쓸 정보만 남겨 반환
        return {"sub": sub, **{k: v for k, v in payload.items() if k not in {"sub", "exp"}}}
    except JWTError:
        raise cred_exc
