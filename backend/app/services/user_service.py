from sqlalchemy import Connection

from app.models import User


def create_user(connection: Connection, name: str):
    result = connection.execute(
        User.__table__.insert().values(name=name)
    )

    user_id = result.inserted_primary_key[0]

    return {
        "id": user_id,
        "name": name
    }

def get_users(connection: Connection):
    result = connection.execute(
        User.__table__.select()
    )

    users = []

    for user in result:
        users.append({
            "id": user.id,
            "name": user.name
        })

    return users

def get_user(connection: Connection, user_id: int):
    result = connection.execute(
        User.__table__.select().where(User.id == user_id)
    )

    user = result.fetchone()

    if user is None:
        return None

    return {
        "id": user.id,
        "name": user.name
    }

def delete_user(connection: Connection, user_id: int):
    result = connection.execute(
        User.__table__.delete().where(User.id == user_id)
    )

    return result.rowcount > 0

def update_user(connection: Connection, user_id: int, name: str):
    result = connection.execute(
        User.__table__
        .update()
        .where(User.id == user_id)
        .values(name=name)
    )

    if result.rowcount == 0:
        return None

    return {
        "id": user_id,
        "name": name
    }
