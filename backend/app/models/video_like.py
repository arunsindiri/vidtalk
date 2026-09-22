from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from app.database import Base


class VideoLike(Base):
    __tablename__ = "video_likes"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "video_id",
            name="uq_user_video_like"
        ),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
