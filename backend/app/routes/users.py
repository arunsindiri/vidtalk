from fastapi import APIRouter

from app.database import engine
from app.schemas import UserCreate, UserResponse
from app.services.user_service import create_user, get_users


router = APIRouter()

@router.post("/users", response_model=list[UserResponse])
def create_user_route(user: UserCreate):
    with engine.begin() as connection:
        return create_user(connection, user.name)

@router.get("/users")
def get_users_route():
    with engine.connect() as connection:
        return get_users(connection)
