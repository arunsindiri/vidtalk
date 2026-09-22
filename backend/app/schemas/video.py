from datetime import datetime
from pydantic import BaseModel


class VideoCreate(BaseModel):
    title: str
    description: str | None = None
    video_url: str
    duration: int


class VideoResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str | None
    video_url: str
    duration: int
    created_at: datetime
    like_count: int
    has_liked: bool
    

class VideoUpdate(BaseModel):
    title: str
    description: str | None = None
    video_url: str
    duration: int

