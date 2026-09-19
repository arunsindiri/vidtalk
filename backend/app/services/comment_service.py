from datetime import datetime

from sqlalchemy import Connection

from app.models import Comment


def create_comment(
    connection: Connection,
    user_id: int,
    video_id: int,
    text: str,
    timestamp: int | None,
    parent_comment_id: int | None,
):
    result = connection.execute(
        Comment.__table__.insert()
        .values(
            user_id=user_id,
            video_id=video_id,
            text=text,
            timestamp=timestamp,
            parent_comment_id=parent_comment_id,
            created_at=datetime.now(),
        )
        .returning(Comment.__table__)
    )

    comment = result.fetchone()

    return dict(comment._mapping)


def get_comments_by_video(connection: Connection, video_id: int):
    result = connection.execute(
        Comment.__table__
        .select()
        .where(Comment.video_id == video_id)
    )

    comments = []

    for comment in result:
        comments.append(dict(comment._mapping))

    return comments
