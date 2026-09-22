from datetime import datetime

from sqlalchemy import Connection, func
from sqlalchemy.exc import IntegrityError

from app.models import VideoLike, User, Video


def create_like(
    connection: Connection,
    user_id: int,
    video_id: int,
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

    try:
        result = connection.execute(
            VideoLike.__table__.insert()
            .values(
                user_id=user_id,
                video_id=video_id,
                created_at=datetime.now(),
            )
            .returning(VideoLike.__table__)
        )
    except IntegrityError:
        return "duplicate"

    like = result.fetchone()

    return dict(like._mapping)


def get_like_count(
    connection: Connection,
    video_id: int,
):
    result = connection.execute(
        VideoLike.__table__
        .select()
        .with_only_columns(
            func.count(VideoLike.id)
        )
        .where(VideoLike.video_id == video_id)
    )

    return result.scalar()


def has_user_liked(
    connection: Connection,
    user_id: int,
    video_id: int,
):
    result = connection.execute(
        VideoLike.__table__
        .select()
        .where(
            VideoLike.user_id == user_id,
            VideoLike.video_id == video_id,
        )
    )

    return result.fetchone() is not None


def delete_like(
    connection: Connection,
    user_id: int,
    video_id: int,
):
    result = connection.execute(
        VideoLike.__table__
        .delete()
        .where(
            VideoLike.user_id == user_id,
            VideoLike.video_id == video_id,
        )
    )

    if result.rowcount == 0:
        return None

    return True
