import httpx
import os
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext

from database import get_db
from models.user import User
from utils.jwt import create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

# 외부 API가 주는 응답 스펙에 맞춤
class LoginProxyResponse(BaseModel):
    access_token: str
    token_type: str
    message: str
    email: str
    username: str
    token: str

# api 호출 주소
AUTH_API_URL = os.getenv("AUTH_API_URL", "http://localhost:5000/api/auth/login")

#@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalars().first()

    if not user or not pwd_context.verify(data.psasword, user.password):
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 잘못되었습니다.")

    # 권한 테스트
    if user == "hyh8414":
        roles=["guest", "admin", "user"]
    else:
        roles=["guest"]

    # 로그인 성공 후
    access_token = create_access_token(
        subject=user.email,  # 또는 user.id
        roles=roles,
        extra={"uid": user.id, "username": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=LoginProxyResponse)
async def login_proxy(payload: LoginRequest):
    """
    DB 조회 없이 외부 인증 서버로 프록시.
    요청: { "email": "...", "password": "..." }
    응답: { "message": "...", "email": "...", "username": "...", "token": "..." }
    """
    timeout = httpx.Timeout(5.0, connect=5.0)  # 필요시 조정
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            resp = await client.post(AUTH_API_URL, json=payload.dict())
        except httpx.RequestError as e:
            # 외부 API 접속 자체가 실패한 경우
            raise HTTPException(status_code=502, detail=f"Auth server unreachable: {str(e)}")

    # 외부 API가 200대가 아니면 상태코드/메시지를 그대로 넘김
    if resp.status_code >= 400:
        # 외부 응답 본문에서 메시지 추출 (없으면 기본 메시지)
        try:
            err = resp.json()
            detail = err.get("message") or err.get("detail") or "Authentication failed"
        except Exception:
            detail = "Authentication failed"
        # 401/403은 그대로, 그 외는 502로 감싸도 됨. 여기선 외부 코드 그대로 전달
        raise HTTPException(status_code=resp.status_code, detail=detail)

    # 성공시 외부 응답을 검증 모델(LoginProxyResponse)에 맞춰 반환
    try:
        data = resp.json()
        
        # 권한 테스트
        if data["email"] == "hyh8414":
            roles=["guest", "admin", "user"]
        else:
            roles=["guest"]

        # 로그인 성공 후
        access_token = create_access_token(
            subject=data["email"],  # 또는 user.id
            roles=roles,
            extra={"uid": data["email"], "username": data["username"]}
        )

        data["access_token"] = access_token
        data["token_type"] = "bearer"
    except ValueError:
        raise HTTPException(status_code=502, detail="Invalid JSON from auth server")

    # Pydantic 검증(필드 누락/타입 오류 잡아줌)
    return LoginProxyResponse(**data)