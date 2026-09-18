from fastapi import APIRouter


from app.services.video_service import create_video, get_videos
from app.schemas import VideoCreate, VideoResponse
from app.database import engine


router = APIRouter()


@router.post("/videos", response_model=VideoResponse)
def create_video_route(video: VideoCreate):
    with engine.begin() as connection:
        return create_video(
            connection,
            video.user_id,
            video.title,
            video.description,
            video.video_url
        )


@router.get("/videos", response_model=list[VideoResponse])
def get_videos_route():
    with engine.connect() as connection:
        return get_videos(connection)
