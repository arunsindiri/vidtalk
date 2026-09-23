from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    text = Column(String, nullable=True)
    video_url = Column(String, nullable=True)
    timestamp = Column(Integer, nullable=True)
    parent_comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    created_at = Column(DateTime, nullable=False)
