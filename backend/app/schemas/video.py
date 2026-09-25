from datetime import datetime
from pydantic import BaseModel


class VideoResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str | None
    video_url: str
    duration: int
    created_at: datetime
    

class VideoFeedResponse(VideoResponse):
    like_count: int
    has_liked: bool
