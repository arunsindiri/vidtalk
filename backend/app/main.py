from app.routes.users import router as users_router
from app.routes.videos import router as videos_router
from app.routes.comments import router as comments_router
from app.routes.auth import router as auth_router
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY")
)

app.include_router(users_router)
app.include_router(videos_router)
app.include_router(comments_router)
app.include_router(auth_router)



@app.get("/hello")
def hello():
    return {"message": "Hello from VidTalk!"}


