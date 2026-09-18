from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    video_url = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
