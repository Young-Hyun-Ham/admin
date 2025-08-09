# .env 파일 로딩 및 공통 모듈 초기화
from dotenv import load_dotenv

# 환경 변수를 사용하는 다른 모듈보다 먼저 로드
load_dotenv()

# 공통적으로 사용할 DB 세션, JWT 유틸
from .database import SessionLocal, engine
from .utils.jwt import create_access_token, verify_token

# 예: 앱 레벨에서 공통 로그 설정
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend")
