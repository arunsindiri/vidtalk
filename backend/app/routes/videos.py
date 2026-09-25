from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from app.auth.dependencies import get_current_user_id
from app.services.video_service import create_video, get_videos, get_video, update_video, delete_video, get_videos_by_user, search_videos
from app.database import engine
from app.services.video_like_service import (
    create_like,
    get_like_count,
    has_user_liked,
    delete_like,
)
from app.services.cloudinary_service import upload_video
from app.schemas import (
    VideoResponse,
    VideoFeedResponse,
    VideoLikeResponse,
)

router = APIRouter()


@router.post("/videos", response_model=VideoResponse)
def create_video_route(
    title: str = Form(...),
    description: str | None = Form(None),
    file: UploadFile = File(...),
    current_user_id: int = Depends(get_current_user_id)
):    
    if file.content_type != "video/mp4":
        raise HTTPException(
            status_code=400,
            detail="Only MP4 videos are allowed"
        )

    result = upload_video(file.file)
    
    with engine.begin() as connection:
        return create_video(
            connection,
            current_user_id,
            title,
            description,
            result["secure_url"],
            result["public_id"],
            int(result["duration"])
        )


@router.post(
    "/videos/{video_id}/like",
    response_model=VideoLikeResponse
)
def create_like_route(
    video_id: int,
    current_user_id: int = Depends(get_current_user_id)
):
    with engine.begin() as connection:
        created_like = create_like(
            connection,
            current_user_id,
            video_id
        )

    if created_like == "duplicate":
        raise HTTPException(
            status_code=409,
            detail="You have already liked this video"
        )

    if created_like is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid user or video"
        )

    return created_like


@router.delete("/videos/{video_id}/like")
def delete_like_route(
    video_id: int,
    current_user_id: int = Depends(get_current_user_id)
):
    with engine.begin() as connection:
        deleted = delete_like(
            connection,
            current_user_id,
            video_id
        )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Like not found"
        )

    return {"message": "Video unliked successfully"}


@router.get("/videos/{video_id}/likes/count")
def get_like_count_route(video_id: int):
    with engine.connect() as connection:
        video = get_video(connection, video_id)

        if video is None:
            raise HTTPException(
                status_code=404,
                detail="Video not found"
            )

        like_count = get_like_count(
            connection,
            video_id
        )

    return {
        "video_id": video_id,
        "like_count": like_count
    }


@router.get("/videos/{video_id}/like-status")
def get_like_status_route(
    video_id: int,
    current_user_id: int = Depends(get_current_user_id)
):
    with engine.connect() as connection:
        video = get_video(connection, video_id)

        if video is None:
            raise HTTPException(
                status_code=404,
                detail="Video not found"
            )

        has_liked = has_user_liked(
            connection,
            current_user_id,
            video_id
        )

    return {
        "video_id": video_id,
        "user_id": current_user_id,
        "has_liked": has_liked
    }


@router.get("/videos", response_model=list[VideoFeedResponse])
def get_videos_route(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user_id: int = Depends(get_current_user_id)
):
    with engine.connect() as connection:
        return get_videos(
            connection,
            skip,
            limit,
            current_user_id
        )


@router.get("/videos/search", response_model=list[VideoFeedResponse])
def search_videos_route(
    q: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user_id: int = Depends(get_current_user_id)
):
    with engine.connect() as connection:
        return search_videos(
            connection,
            q,
            skip,
            limit,
            current_user_id
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
    title: str = Form(...),
    description: str | None = Form(None),
    file: UploadFile = File(...),
    current_user_id: int = Depends(get_current_user_id)
):

    if file.content_type != "video/mp4":
        raise HTTPException(
            status_code=400,
            detail="Only MP4 videos are allowed"
        )

    result = upload_video(file.file)

    with engine.begin() as connection:
        updated_video = update_video(
            connection,
            video_id,
            current_user_id,
            title,
            description,
            result["secure_url"],
            result["public_id"],
            int(result["duration"])
        )

    if updated_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    
    if updated_video == "forbidden":
        raise HTTPException(status_code=403, detail="You do not own this video")
    
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

    if deleted is None:
        raise HTTPException(status_code=404, detail="Video not found")
    
    if deleted == "forbidden":
        raise HTTPException(status_code=403, detail="You do not own this video")
    
    return {"message": "Video deleted successfully"}


@router.get("/users/{user_id}/videos", response_model=list[VideoResponse])
def get_videos_by_user_route(user_id: int):
    with engine.connect() as connection:
        return get_videos_by_user(connection, user_id)


