from passlib.context import CryptContext

# bcrypt를 사용한 암호화 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 평문 비밀번호
raw_password = "1234"

# 비밀번호 해시 생성
hashed_password = pwd_context.hash(raw_password)

# 출력
print(f"평문 비밀번호: {raw_password}")
print(f"해시된 비밀번호: {hashed_password}")
