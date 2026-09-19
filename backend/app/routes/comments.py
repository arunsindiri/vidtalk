from fastapi import APIRouter

from app.database import engine
from app.schemas import CommentCreate, CommentResponse
from app.services.comment_service import create_comment, get_comments_by_video


router = APIRouter()


@router.post("/comments", response_model=CommentResponse)
def create_comment_route(comment: CommentCreate):
    with engine.begin() as connection:
        return create_comment(
            connection,
            comment.user_id,
            comment.video_id,
            comment.text,
            comment.timestamp,
            comment.parent_comment_id
        )


@router.get("/videos/{video_id}/comments", response_model=list[CommentResponse])
def get_comments_by_video_route(video_id: int):
    with engine.connect() as connection:
        return get_comments_by_video(connection, video_id)
