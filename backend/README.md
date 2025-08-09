# FastAPI Backend 프로젝트

이 프로젝트는 FastAPI를 기반으로 한 간단한 REST API 서버 예제입니다. 메뉴 정보를 등록하고 조회할 수 있는 기능을 포함하고 있습니다.

---

## 📦 설치 방법

아래 명령어를 통해 필요한 패키지를 설치하세요.

```bash
pip install fastapi uvicorn
```

선택적으로 `requirements.txt` 파일을 만들어서 다음 내용을 추가할 수 있습니다:

```
# FastAPI 웹 프레임워크
fastapi==0.111.0

# ASGI 서버 (FastAPI 실행용)
uvicorn[standard]==0.30.1

# 데이터베이스 ORM 라이브러리
SQLAlchemy==2.0.31

# PostgreSQL 데이터베이스 드라이버
psycopg2-binary==2.9.9

# 환경변수(.env) 관리
python-dotenv==1.0.1

# 비밀번호 해싱 및 검증 라이브러리 (bcrypt 포함)
passlib[bcrypt]==1.7.4
bcrypt==3.2.2   # Passlib과 호환되는 안정 버전

# 데이터 유효성 검사 라이브러리 (FastAPI에서 사용)
pydantic==2.7.1
pydantic-settings==2.2.1

# (선택) 로그 출력 향상 라이브러리
loguru==0.7.2

# AI ( langchain, langsmith[추적] )
openai
langsmith
langchain
langchain-community
langchain-openai
langchain-teddynote

# PostgreSQL 백터 사용을 위한 확장 라이브러리
pgvector
```

그 후:

```bash
pip install -r requirements.txt
```

---

## 🚀 실행 방법

다음 명령어로 서버를 실행합니다:

```bash
uvicorn main:app --reload
```

서버가 실행되면 아래 주소로 접속할 수 있습니다:

- Swagger 문서: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc 문서: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---
```
# pip을 최신 버전으로 업그레이드
python -m pip install --upgrade pip
# requirements.txt에 정의된 모든 패키지를 설치
python -m pip install -r requirements.txt

# 디렉토리 초기 구조
backend/
├── auth/
│   ├── jwt.py              # JWT 생성/검증 유틸
│   └── dependencies.py     # 현재 사용자 확인
├── crud/
│   └── user_crud.py        # 로그인 검증 등 DB 연동
├── models/
│   └── user.py             # SQLAlchemy 모델
├── schemas/
│   └── user_schema.py      # Pydantic 모델
├── routers/
│   └── auth.py             # 로그인 엔드포인트
├── database.py
├── main.py
└── .env

# AI CHAT 디렉토리 초기 구조
backend/
├── app/                    # AI CHAT 관련
│   ├── routes/
│   │   └── chat.py         
│   │   └── docs.py         
│   ├── chat_service.py     # 채팅 서비스 로직
│   ├── config.py           
│   ├── database.py         # 확장/테이블 준비
│   ├── main.py             
│   ├── models.py           # SQLAlchemy 모델
│   ├── reg_service.py      #
│   └── schemas.py          # Pydantic 모델
└── .env
```
