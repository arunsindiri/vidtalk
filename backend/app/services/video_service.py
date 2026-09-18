from datetime import datetime

from sqlalchemy import Connection

from app.models import Video


def create_video(
    connection: Connection,
    user_id: int,
    title: str,
    description: str | None,
    video_url: str,
):
    result = connection.execute(
        Video.__table__.insert()
        .values(
            user_id=user_id,
            title=title,
            description=description,
            video_url=video_url,
            created_at=datetime.now(),
        )
        .returning(Video.__table__)
    )

    video = result.fetchone()

    return dict(video._mapping)


def get_videos(connection: Connection):
    result = connection.execute(
        Video.__table__.select()
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
    title: str,
    description: str | None,
    video_url: str,
):
    result = connection.execute(
        Video.__table__
        .update()
        .where(Video.id == video_id)
        .values(
            title=title,
            description=description,
            video_url=video_url,
        )
        .returning(Video.__table__)
    )

    video = result.fetchone()

    if video is None:
        return None

    return dict(video._mapping)


def delete_video(connection: Connection, video_id: int):
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
