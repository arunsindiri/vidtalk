from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from app.database import Base


class CommentReaction(Base):
    __tablename__ = "comment_reactions"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "comment_id",
            name="uq_user_comment_reaction"
        ),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
