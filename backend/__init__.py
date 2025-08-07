
# 공통적으로 사용할 DB 세션, JWT 유틸, 환경변수 로딩
from .database import SessionLocal, engine
from .utils.jwt import create_access_token, verify_token
from dotenv import load_dotenv

# .env 파일 로딩

# 예: 앱 레벨에서 공통 로그 설정
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend")
