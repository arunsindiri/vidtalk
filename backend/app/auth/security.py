SECRET_KEY = "dev-secret-key-change-later-12345"

ALGORITHM = "HS256"

import jwt

from datetime import datetime, timedelta, timezone

from jwt.exceptions import InvalidTokenError


def create_access_token(user_id: int):
    expiration = datetime.now(timezone.utc) + timedelta(minutes=30)
    
    payload = {
        "user_id": user_id,
        "exp": expiration
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def decode_access_token(token: str): 
    try:   
        payload = jwt.decode(
            token, 
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except InvalidTokenError:
        return None
