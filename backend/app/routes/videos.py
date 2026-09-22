from fastapi import APIRouter, Depends, HTTPException, Query
from app.auth.dependencies import get_current_user_id
from app.services.video_service import create_video, get_videos, get_video, update_video, delete_video, get_videos_by_user, search_videos
from app.schemas import VideoCreate, VideoResponse, VideoUpdate
from app.database import engine


router = APIRouter()


@router.post("/videos", response_model=VideoResponse)
def create_video_route(
    video: VideoCreate,
    current_user_id: int = Depends(get_current_user_id)
):
    with engine.begin() as connection:
        return create_video(
            connection,
            current_user_id,
            video.title,
            video.description,
            video.video_url,
            video.duration
        )


@router.get("/videos", response_model=list[VideoResponse])
def get_videos_route(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    with engine.connect() as connection:
        return get_videos(connection, skip, limit)


@router.get("/videos/search", response_model=list[VideoResponse])
def search_videos_route(
    q: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    with engine.connect() as connection:
        return search_videos(
            connection,
            q,
            skip,
            limit
        )


@router.get("/videos/{video_id}", response_model=VideoResponse)
def get_video_route(video_id: int):
    with engine.connect() as connection:
        video = get_video(connection, video_id)

    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")

    return video


@router.put("/videos/{video_id}", response_model=VideoResponse)
def update_video_route(
    video_id: int,
    video: VideoUpdate,
    current_user_id: int = Depends(get_current_user_id)
):
    with engine.begin() as connection:
        updated_video = update_video(
            connection,
            video_id,
            current_user_id,
            video.title,
            video.description,
            video.video_url,
            video.duration
        )

    if updated_video is None:
        raise HTTPException(status_code=404, detail="Video not found")

    return updated_video


@router.delete("/videos/{video_id}")
def delete_video_route(
    video_id: int,
    current_user_id: int = Depends(get_current_user_id)
):
    with engine.begin() as connection:
        deleted = delete_video(
            connection,
            video_id,
            current_user_id
        )

    if not deleted:
        raise HTTPException(status_code=404, detail="Video not found")

    return {"message": "Video deleted successfully"}


@router.get("/users/{user_id}/videos", response_model=list[VideoResponse])
def get_videos_by_user_route(user_id: int):
    with engine.connect() as connection:
        return get_videos_by_user(connection, user_id)
