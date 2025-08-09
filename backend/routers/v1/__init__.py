from .auth import router as auth_router
from .board import router as board_router

# 여기에 추가 라우터들을 계속 등록
__all__ = ["v1_routers"]

v1_routers = [
    auth_router,
    board_router,
]
