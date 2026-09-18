from fastapi import APIRouter, HTTPException

from app.database import engine
from app.schemas import UserCreate, UserResponse
from app.services.user_service import create_user, get_users, get_user


router = APIRouter()

@router.post("/users", response_model=UserResponse)
def create_user_route(user: UserCreate):
    with engine.begin() as connection:
        return create_user(connection, user.name)

@router.get("/users", response_model=list[UserResponse])
def get_users_route():
    with engine.connect() as connection:
        return get_users(connection)

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_route(user_id: int):
    with engine.connect() as connection:
        user = get_user(connection, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user
        
