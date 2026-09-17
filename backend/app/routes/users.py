from fastapi import APIRouter

from app.database import engine
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.services.user_service import create_user


router = APIRouter()

@router.post("/users", response_model=UserResponse)
def create_user_route(user: UserCreate):
    with engine.begin() as connection:
        return create_user(connection, user.name)

@router.get("/users")
def get_users():
    with engine.connect() as connection:
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
