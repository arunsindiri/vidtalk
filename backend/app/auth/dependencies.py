from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.security import decode_access_token
from app.database import engine
from app.services.user_service import get_user

bearer_scheme = HTTPBearer()


def get_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    return credentials.credentials


def get_current_user_id(
    token: str = Depends(get_token)
):
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user_id = payload.get("user_id")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    with engine.connect() as connection:
        user = get_user(connection, user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user["id"]
