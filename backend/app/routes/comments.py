from fastapi import APIRouter, HTTPException

from app.database import engine
from app.schemas import CommentCreate, CommentResponse, CommentUpdate, ReplyCreate
from app.services.comment_service import (
    create_comment,
    get_comments_by_video,
    get_comment,
    update_comment,
    delete_comment,
    create_reply,
)


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


@router.get("/comments/{comment_id}", response_model=CommentResponse)
def get_comment_route(comment_id: int):
    with engine.connect() as connection:
        comment = get_comment(connection, comment_id)

    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    return comment


@router.put("/comments/{comment_id}", response_model=CommentResponse)
def update_comment_route(comment_id: int, comment: CommentUpdate):
    with engine.begin() as connection:
        updated_comment = update_comment(
            connection,
            comment_id,
            comment.text,
            comment.timestamp
        )

    if updated_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    return updated_comment


@router.delete("/comments/{comment_id}")
def delete_comment_route(comment_id: int):
    with engine.begin() as connection:
        deleted = delete_comment(connection, comment_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Comment not found")

    return {"message": "Comment deleted successfully"}


@router.post(
    "/comments/{comment_id}/replies",
    response_model=CommentResponse
)
def create_reply_route(
    comment_id: int,
    reply: ReplyCreate
):
    with engine.begin() as connection:
        created_reply = create_reply(
            connection,
            reply.user_id,
            comment_id,
            reply.text,
            reply.timestamp
        )

    if created_reply is None:
        raise HTTPException(
            status_code=404,
            detail="Parent comment not found"
        )

    return created_reply
