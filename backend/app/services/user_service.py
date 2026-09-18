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
