from datetime import datetime

from pydantic import BaseModel


class ReactionCreate(BaseModel):
    user_id: int
    comment_id: int


class ReactionResponse(BaseModel):
    id: int
    user_id: int
    comment_id: int
    created_at: datetime
