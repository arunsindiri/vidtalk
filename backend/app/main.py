from app.schemas import UserCreate, UserResponse
from fastapi import FastAPI
from app.database import engine
from app.models import User

app = FastAPI()



@app.get("/hello")
def hello():
    return {"message": "Hello from VidTalk!"}



@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    with engine.begin() as connection:
        result = connection.execute(
            User.__table__.insert().values(name=user.name)
        )

        user_id = result.inserted_primary_key[0]

    return {
        "id": user_id,
        "name": user.name
    }


@app.get("/users")
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
