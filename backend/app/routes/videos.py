from fastapi import APIRouter, HTTPException


from app.services.video_service import create_video, get_videos, get_video
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


@router.get("/videos/{video_id}", response_model=VideoResponse)
def get_video_route(video_id: int):
    with engine.connect() as connection:
        video = get_video(connection, video_id)

    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")

    return video
