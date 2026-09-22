from datetime import datetime

from pydantic import BaseModel


class VideoLikeResponse(BaseModel):
    id: int
    user_id: int
    video_id: int
    created_at: datetime
