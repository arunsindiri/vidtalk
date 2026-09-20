from datetime import datetime

from sqlalchemy import Connection

from app.models import Comment, Video, User


def create_comment(
    connection: Connection,
    user_id: int,
    video_id: int,
    text: str,
    timestamp: int | None,
    parent_comment_id: int | None,
):

    user = connection.execute(
        User.__table__
        .select()
        .where(User.id == user_id)
    ).fetchone()

    if user is None:
        return None
    
    video = connection.execute(
        Video.__table__
        .select()
        .where(Video.id == video_id)
    ).fetchone()

    if video is None:
        return None
    
    if timestamp is not None and (
        timestamp < 0 or timestamp > video.duration
    ):
        return None
    
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


def get_comments_by_video(
    connection: Connection,
    video_id: int,
    skip: int,
    limit: int,
):
    result = connection.execute(
        Comment.__table__
        .select()
        .where(Comment.video_id == video_id)
        .order_by(Comment.created_at)
        .offset(skip)
        .limit(limit)
    )

    comments = []

    for comment in result:
        comments.append(dict(comment._mapping))

    return comments


def get_comment(connection: Connection, comment_id: int):
    result = connection.execute(
        Comment.__table__
        .select()
        .where(Comment.id == comment_id)
    )

    comment = result.fetchone()

    if comment is None:
        return None

    return dict(comment._mapping)


def update_comment(
    connection: Connection,
    comment_id: int,
    user_id: int,
    text: str,
    timestamp: int | None,
):
    comment = get_comment(connection, comment_id)

    if comment is None:
        return None

    if comment["user_id"] != user_id:
        return "unauthorized"

    video = connection.execute(
        Video.__table__
        .select()
        .where(Video.id == comment["video_id"])
    ).fetchone()

    if video is None:
        return None

    if timestamp is not None and (
        timestamp < 0 or timestamp > video.duration
    ):
        return "invalid_timestamp"

    result = connection.execute(
        Comment.__table__
        .update()
        .where(Comment.id == comment_id)
        .values(
            text=text,
            timestamp=timestamp,
        )
        .returning(Comment.__table__)
    )
    
    updated_comment = result.fetchone()
    
    return dict(updated_comment._mapping)


def delete_comment(
    connection: Connection,
    comment_id: int,
    user_id: int,
):

    comment = get_comment(connection, comment_id)

    if comment is None:
        return None

    if comment["user_id"] != user_id:
        return "unauthorized"
    
    result = connection.execute(
        Comment.__table__
        .delete()
        .where(Comment.id == comment_id)
    )

    return result.rowcount > 0


def create_reply(
    connection: Connection,
    user_id: int,
    parent_comment_id: int,
    text: str,
    timestamp: int | None,
):
    user = connection.execute(
        User.__table__
        .select()
        .where(User.id == user_id)
    ).fetchone()

    if user is None:
        return None
    
    parent_comment = get_comment(connection, parent_comment_id)

    if parent_comment is None:
        return None

    video = connection.execute(
        Video.__table__
        .select()
        .where(Video.id == parent_comment["video_id"])
    ).fetchone()

    if video is None:
        return None

    if timestamp is not None and (
        timestamp < 0 or timestamp > video.duration
    ):
        return None

    result = connection.execute(
        Comment.__table__.insert()
        .values(
            user_id=user_id,
            video_id=parent_comment["video_id"],
            text=text,
            timestamp=timestamp,
            parent_comment_id=parent_comment_id,
            created_at=datetime.now(),
        )
        .returning(Comment.__table__)
    )

    reply = result.fetchone()

    return dict(reply._mapping)


def get_replies(
    connection: Connection,
    parent_comment_id: int,
):
    result = connection.execute(
        Comment.__table__
        .select()
        .where(
            Comment.parent_comment_id == parent_comment_id
        )
    )

    replies = []

    for reply in result:
        replies.append(dict(reply._mapping))

    return replies
    

def video_exists(
    connection: Connection,
    video_id: int,
):
    result = connection.execute(
        Video.__table__
        .select()
        .where(Video.id == video_id)
    )

    return result.fetchone() is not None
    

def get_all_comments_by_video(
    connection: Connection,
    video_id: int,
):
    result = connection.execute(
        Comment.__table__
        .select()
        .where(Comment.video_id == video_id)
        .order_by(Comment.created_at)
    )

    comments = []

    for comment in result:
        comments.append(dict(comment._mapping))

    return comments


def build_comment_tree(comments):
    comments_by_id = {}

    for comment in comments:
        comments_by_id[comment["id"]] = {
            **comment,
            "replies": []
        }

    for comment in comments:
        parent_id = comment["parent_comment_id"]

        if parent_id is not None:
            comments_by_id[parent_id]["replies"].append(
                comments_by_id[comment["id"]]
            )

    return [
        comment
        for comment in comments_by_id.values()
        if comment["parent_comment_id"] is None
    ]
