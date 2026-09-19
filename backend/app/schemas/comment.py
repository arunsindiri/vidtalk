from datetime import datetime

from pydantic import BaseModel


class CommentCreate(BaseModel):
    user_id: int
    video_id: int
    text: str
    timestamp: int | None = None
    parent_comment_id: int | None = None


class CommentResponse(BaseModel):
    id: int
    user_id: int
    video_id: int
    text: str
    timestamp: int | None
    parent_comment_id: int | None
    created_at: datetime
