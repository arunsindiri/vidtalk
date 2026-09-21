from datetime import datetime

from pydantic import BaseModel


class ReactionResponse(BaseModel):
    id: int
    user_id: int
    comment_id: int
    created_at: datetime


class CommentWithReactionResponse(BaseModel):
    id: int
    user_id: int
    video_id: int
    text: str
    timestamp: int | None
    parent_comment_id: int | None
    created_at: datetime
    reaction_count: int
    has_reacted: bool


class CommentTreeWithReactionResponse(CommentWithReactionResponse):
    replies: list["CommentTreeWithReactionResponse"] = []
