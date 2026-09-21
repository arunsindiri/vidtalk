from fastapi import APIRouter, Depends, HTTPException, Query
from app.auth.dependencies import get_current_user_id

from app.database import engine
from app.schemas import (
    CommentCreate,
    CommentResponse,
    CommentUpdate,
    CommentDelete,
    CommentTreeResponse,
    ReplyCreate,
    CommentWithReactionResponse,
    CommentTreeWithReactionResponse,
)
from app.services.comment_service import (
    create_comment,
    get_comments_by_video,
    get_all_comments_by_video,
    build_comment_tree,
    video_exists,
    get_comment,
    update_comment,
    delete_comment,
    create_reply,
    get_replies,
)
from app.schemas import ReactionCreate, ReactionResponse
from app.services.comment_reaction_service import (
    create_reaction,
    get_reaction_count,
    has_user_reacted,
    delete_reaction,
    add_reaction_data_to_tree,
)

router = APIRouter()


@router.post("/comments", response_model=CommentResponse)
def create_comment_route(
    comment: CommentCreate,
    current_user_id: int = Depends(get_current_user_id)
):
    with engine.begin() as connection:
        created_comment = create_comment(
            connection,
            current_user_id,
            comment.video_id,
            comment.text,
            comment.timestamp,
            comment.parent_comment_id
        )

    if created_comment is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid video or timestamp"
        )

    return created_comment


@router.get("/videos/{video_id}/comments", response_model=list[CommentWithReactionResponse])
def get_comments_by_video_route(
    video_id: int,
    current_user_id: int = Depends(get_current_user_id),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    with engine.connect() as connection:
        comments = get_comments_by_video(
            connection,
            video_id,
            skip,
            limit
        )

        for comment in comments:
            comment["reaction_count"] = get_reaction_count(
                connection,
                comment["id"]
            )

            comment["has_reacted"] = has_user_reacted(
                connection,
                current_user_id,
                comment["id"]
            )

    return comments


@router.get("/comments/{comment_id}", response_model=CommentResponse)
def get_comment_route(comment_id: int):
    with engine.connect() as connection:
        comment = get_comment(connection, comment_id)

    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    return comment


@router.put("/comments/{comment_id}", response_model=CommentResponse)
def update_comment_route(
    comment_id: int,
    comment: CommentUpdate,
    current_user_id: int = Depends(get_current_user_id)
):
    with engine.begin() as connection:
        updated_comment = update_comment(
            connection,
            comment_id,
            current_user_id,
            comment.text,
            comment.timestamp
        )

    if updated_comment == "invalid_timestamp":
        raise HTTPException(
            status_code=400,
            detail="Invalid timestamp"
        )

    if updated_comment == "unauthorized":
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to update this comment"
        )
    
    if updated_comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    return updated_comment


@router.delete("/comments/{comment_id}")
def delete_comment_route(
    comment_id: int,
    current_user_id: int = Depends(get_current_user_id)
):
    with engine.begin() as connection:
        deleted = delete_comment(
            connection,
            comment_id,
            current_user_id
        )

    if deleted == "unauthorized":
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to delete this comment"
        )
    
    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    return {"message": "Comment deleted successfully"}


@router.post(
    "/comments/{comment_id}/replies",
    response_model=CommentResponse
)
def create_reply_route(
    comment_id: int,
    reply: ReplyCreate,
    current_user_id: int = Depends(get_current_user_id)
):
    with engine.begin() as connection:
        created_reply = create_reply(
            connection,
            current_user_id,
            comment_id,
            reply.text,
            reply.timestamp
        )

    if created_reply is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid parent comment or timestamp"
        )

    return created_reply


@router.get(
    "/comments/{comment_id}/replies",
    response_model=list[CommentResponse]
)
def get_replies_route(comment_id: int):
    with engine.connect() as connection:
        parent_comment = get_comment(connection, comment_id)

        if parent_comment is None:
            raise HTTPException(
                status_code=404,
                detail="Comment not found"
            )

        return get_replies(connection, comment_id)


@router.get(
    "/videos/{video_id}/comments/tree",
    response_model=list[CommentTreeWithReactionResponse]
)
def get_comments_tree_route(video_id: int, user_id: int):
    with engine.connect() as connection:
    
        if not video_exists(connection, video_id):
            raise HTTPException(
                status_code=404,
                detail="Video not found"
            )

        comments = get_all_comments_by_video(
            connection,
            video_id
        )

        tree = build_comment_tree(comments)
    
        tree = add_reaction_data_to_tree(
            connection,
            tree,
            user_id
        )

        return tree


@router.post(
    "/comments/{comment_id}/reactions",
    response_model=ReactionResponse
)
def create_reaction_route(
    comment_id: int,
    reaction: ReactionCreate,
    current_user_id: int = Depends(get_current_user_id)
):
    with engine.begin() as connection:
        created_reaction = create_reaction(
            connection,
            current_user_id,
            comment_id
        )

    if created_reaction == "duplicate":
        raise HTTPException(
            status_code=409,
            detail="You have already reacted to this comment"
        )

    if created_reaction is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid user or comment"
        )

    return created_reaction


@router.get("/comments/{comment_id}/reactions/count")
def get_reaction_count_route(comment_id: int):
    with engine.connect() as connection:
        comment = get_comment(connection, comment_id)

        if comment is None:
            raise HTTPException(
                status_code=404,
                detail="Comment not found"
            )

        reaction_count = get_reaction_count(
            connection,
            comment_id
        )

    return {
        "comment_id": comment_id,
        "reaction_count": reaction_count
    }


@router.get("/comments/{comment_id}/reactions/status")
def get_reaction_status_route(
    comment_id: int,
    current_user_id: int = Depends(get_current_user_id)
):
    with engine.connect() as connection:
        comment = get_comment(connection, comment_id)

        if comment is None:
            raise HTTPException(
                status_code=404,
                detail="Comment not found"
            )

        has_reacted = has_user_reacted(
            connection,
            current_user_id,
            comment_id
        )

    return {
        "comment_id": comment_id,
        "user_id": current_user_id,
        "has_reacted": has_reacted
    }


@router.delete("/comments/{comment_id}/reactions")
def delete_reaction_route(
    comment_id: int,
    current_user_id: int = Depends(get_current_user_id)
):
    with engine.begin() as connection:
        deleted = delete_reaction(
            connection,
            current_user_id,
            comment_id
        )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Reaction not found"
        )

    return {
        "message": "Reaction removed successfully"
    }
