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


# React Admin Backend

이 프로젝트는 React-Admin 프론트엔드와 연동되는 Node.js 기반의 백엔드입니다.

## 폴더 구조

```
backend/
├── src/                   # 주요 소스 코드
│   ├── controllers/       # API 컨트롤러
│   ├── models/            # DB 모델
│   ├── services/          # 비즈니스 로직
│   ├── routes/            # 라우터
│   └── index.js           # 서버 진입점
├── package.json           # 프로젝트 설정
├── Dockerfile             # 도커 설정
├── .env                   # 환경 변수 파일
├── README.md              # 프로젝트 설명
└── .env
```

## 개발 환경 설정

1. 의존성 설치
	```bash
	npm install
	```

2. 환경 변수 설정
	`.env` 파일을 생성하여 DB 연결 정보 등 환경 변수를 설정합니다.
	예시:
	```env
	DB_HOST=localhost
	DB_PORT=5432
	DB_USER=youruser
	DB_PASS=yourpassword
	DB_NAME=yourdb
	PORT=5003
	```

3. 개발 서버 실행
	```bash
	npm start
	```
	기본 포트는 5003입니다. (환경 변수에서 변경 가능)

4. DB 마이그레이션 및 시드
	```bash
	npm run migrate
	npm run seed
	```
	(스크립트가 존재할 경우)

5. 도커로 실행
	```bash
	docker build -t react-admin-backend .
	docker run -p 5003:5003 --env-file .env react-admin-backend
	```

## 주요 라이브러리

- [Express](https://expressjs.com/) : Node.js 웹 프레임워크
- [Sequelize](https://sequelize.org/) 또는 [TypeORM](https://typeorm.io/) : ORM
- [dotenv](https://github.com/motdotla/dotenv) : 환경 변수 관리
- [pg](https://node-postgres.com/) : PostgreSQL 클라이언트

## API 엔드포인트 예시

- `GET /api/{resource}` : 목록 조회
- `GET /api/{resource}/{id}` : 단일 항목 조회
- `POST /api/{resource}` : 생성
- `PUT /api/{resource}/{id}` : 수정
- `DELETE /api/{resource}/{id}` : 삭제

## 기타

- CORS 설정 필요 시 [cors](https://github.com/expressjs/cors) 미들웨어 사용
- 에러 핸들링 및 로깅을 위한 [morgan](https://github.com/expressjs/morgan) 등 활용

---

프로젝트 구조와 환경 설정에 대해 궁금한 점이 있으면 언제든 문의해 주세요.
```
