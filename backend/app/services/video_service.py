from datetime import datetime

from sqlalchemy import Connection, case, func

from app.models import Video, VideoLike


def create_video(
    connection: Connection,
    user_id: int,
    title: str,
    description: str | None,
    video_url: str,
    duration: int,
):
    result = connection.execute(
        Video.__table__.insert()
        .values(
            user_id=user_id,
            title=title,
            description=description,
            video_url=video_url,
            duration=duration,
            created_at=datetime.now(),
        )
        .returning(Video.__table__)
    )

    video = result.fetchone()

    return dict(video._mapping)


def get_videos(
    connection: Connection,
    skip: int,
    limit: int,
    current_user_id: int
):
    result = connection.execute(
        Video.__table__
        .outerjoin(
            VideoLike.__table__,
            Video.id == VideoLike.video_id
        )
        .select()
        .with_only_columns(
            *Video.__table__.c,
            func.count(VideoLike.id).label("like_count"),
            case(
                (
                    func.count(
                        case(
                            (
                                VideoLike.user_id == current_user_id,
                                1
                            )
                        )
                    ) > 0,
                    True
                ),
                else_=False
            ).label("has_liked")
        )
        .group_by(Video.id)
        .order_by(Video.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    videos = []

    for video in result:
        videos.append(dict(video._mapping))

    return videos


def search_videos(
    connection: Connection,
    query: str,
    skip: int,
    limit: int,
    current_user_id: int
):
    search_pattern = f"%{query}%"

    result = connection.execute(
        Video.__table__
        .outerjoin(
            VideoLike.__table__,
            Video.id == VideoLike.video_id
        )
        .select()
        .with_only_columns(
            *Video.__table__.c,
            func.count(VideoLike.id).label("like_count"),
            (
                func.count(
                    case(
                        (
                            VideoLike.user_id == current_user_id,
                            1
                        )
                    )
                ) > 0
            ).label("has_liked")
        )
        .where(
            Video.title.ilike(search_pattern)
            | Video.description.ilike(search_pattern)
        )
        .group_by(Video.id)
        .order_by(Video.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    videos = []

    for video in result:
        videos.append(dict(video._mapping))

    return videos


def get_video(connection: Connection, video_id: int):
    result = connection.execute(
        Video.__table__.select().where(Video.id == video_id)
    )

    video = result.fetchone()

    if video is None:
        return None

    return dict(video._mapping)


def update_video(
    connection: Connection,
    video_id: int,
    user_id: int,
    title: str,
    description: str | None,
    video_url: str,
    duration: int,
):
    video = connection.execute(
        Video.__table__
        .select()
        .where(Video.id == video_id)
    ).fetchone()

    if video is None:
        return None

    if video.user_id != user_id:
        return "forbidden"

    result = connection.execute(
        Video.__table__
        .update()
        .where(Video.id == video_id)
        .values(
            title=title,
            description=description,
            video_url=video_url,
            duration=duration,
        )
        .returning(Video.__table__)
    )

    updated_video = result.fetchone()

    return dict(updated_video._mapping)


def delete_video(
    connection: Connection,
    video_id: int,
    user_id: int
):
    video = connection.execute(
        Video.__table__
        .select()
        .where(Video.id == video_id)
    ).fetchone()

    if video is None:
        return None

    if video.user_id != user_id:
        return "forbidden"

    result = connection.execute(
        Video.__table__
        .delete()
        .where(Video.id == video_id)
    )

    return result.rowcount > 0


def get_videos_by_user(connection: Connection, user_id: int):
    result = connection.execute(
        Video.__table__.select().where(Video.user_id == user_id)
    )

    videos = []

    for video in result:
        videos.append(dict(video._mapping))

    return videos
