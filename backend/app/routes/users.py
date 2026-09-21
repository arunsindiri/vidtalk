from fastapi import APIRouter, Depends, HTTPException

from app.database import engine
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.services.user_service import create_user, get_users, get_user, delete_user, update_user
from app.auth.dependencies import get_current_user_id


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
        
@router.delete("/users/me")
def delete_user_route(
    current_user_id: int = Depends(get_current_user_id)
):
    with engine.begin() as connection:
        deleted = delete_user(connection, current_user_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}


@router.put("/users/me", response_model=UserResponse)
def update_user_route(
    user: UserUpdate,
    current_user_id: int = Depends(get_current_user_id)
):
    with engine.begin() as connection:
        updated_user = update_user(
            connection,
            current_user_id,
            user.name
        )

    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user
