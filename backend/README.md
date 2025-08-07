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
fastapi
uvicorn
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
│   ├── user_crud.py        # 로그인 검증 등 DB 연동
├── models/
│   ├── user.py             # SQLAlchemy 모델
├── schemas/
│   ├── user_schema.py      # Pydantic 모델
├── routers/
│   ├── auth.py             # 로그인 엔드포인트
├── database.py
├── main.py
└── .env