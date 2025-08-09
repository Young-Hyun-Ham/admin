from sqlalchemy import Column, Integer, String, Text
from backend.database import Base

class Board(Base):
    __tablename__ = "board"   # ← 테이블명 변경

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(Text)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
