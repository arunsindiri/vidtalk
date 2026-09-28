from fastapi import APIRouter, Request
from app.auth.google import oauth
from app.database import engine
from app.services.user_service import (
    get_user_by_google_id,
    create_google_user
)
from app.auth.security import create_access_token


router = APIRouter()


@router.get("/auth/google/login")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth/google/callback", name="google_callback")
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    
    userinfo = token["userinfo"]

    google_id = userinfo["sub"]
    name = userinfo["name"]

    with engine.connect() as connection:
        user = get_user_by_google_id(
            connection,
            google_id
        )

    if user is None:
        with engine.begin() as connection:
            user = create_google_user(
                connection,
                name,
                google_id
            )

    access_token = create_access_token(user["id"])
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
