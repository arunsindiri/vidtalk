from fastapi import APIRouter, HTTPException


from app.services.video_service import create_video, get_videos, get_video, update_video, delete_video, get_videos_by_user
from app.schemas import VideoCreate, VideoResponse, VideoUpdate
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


@router.put("/videos/{video_id}", response_model=VideoResponse)
def update_video_route(video_id: int, video: VideoUpdate):
    with engine.begin() as connection:
        updated_video = update_video(
            connection,
            video_id,
            video.title,
            video.description,
            video.video_url
        )

    if updated_video is None:
        raise HTTPException(status_code=404, detail="Video not found")

    return updated_video


@router.delete("/videos/{video_id}")
def delete_video_route(video_id: int):
    with engine.begin() as connection:
        deleted = delete_video(connection, video_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Video not found")

    return {"message": "Video deleted successfully"}


@router.get("/users/{user_id}/videos", response_model=list[VideoResponse])
def get_videos_by_user_route(user_id: int):
    with engine.connect() as connection:
        return get_videos_by_user(connection, user_id)
