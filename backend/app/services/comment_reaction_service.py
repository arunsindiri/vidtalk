from datetime import datetime

from sqlalchemy import Connection, func
from sqlalchemy.exc import IntegrityError

from app.models import CommentReaction, User, Comment


def create_reaction(
    connection: Connection,
    user_id: int,
    comment_id: int,
):
    user = connection.execute(
        User.__table__
        .select()
        .where(User.id == user_id)
    ).fetchone()

    if user is None:
        return None

    comment = connection.execute(
        Comment.__table__
        .select()
        .where(Comment.id == comment_id)
    ).fetchone()

    if comment is None:
        return None

    try:
        result = connection.execute(
            CommentReaction.__table__.insert()
            .values(
                user_id=user_id,
                comment_id=comment_id,
                created_at=datetime.now(),
            )
            .returning(CommentReaction.__table__)
        )
    except IntegrityError:
        return "duplicate"

    reaction = result.fetchone()

    return dict(reaction._mapping)


def get_reaction_count(
    connection: Connection,
    comment_id: int,
):
    result = connection.execute(
        CommentReaction.__table__
        .select()
        .with_only_columns(
            func.count(CommentReaction.id)
        )
        .where(CommentReaction.comment_id == comment_id)
    )

    return result.scalar()


def has_user_reacted(
    connection: Connection,
    user_id: int,
    comment_id: int,
):
    result = connection.execute(
        CommentReaction.__table__
        .select()
        .where(
            CommentReaction.user_id == user_id,
            CommentReaction.comment_id == comment_id,
        )
    )

    return result.fetchone() is not None


def delete_reaction(
    connection: Connection,
    user_id: int,
    comment_id: int,
):
    result = connection.execute(
        CommentReaction.__table__
        .delete()
        .where(
            CommentReaction.user_id == user_id,
            CommentReaction.comment_id == comment_id,
        )
    )

    if result.rowcount == 0:
        return None

    return True
