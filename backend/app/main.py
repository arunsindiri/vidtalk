from app.routes.users import router as users_router
from app.routes.videos import router as videos_router
from app.routes.comments import router as comments_router
from fastapi import FastAPI


app = FastAPI()

app.include_router(users_router)
app.include_router(videos_router)
app.include_router(comments_router)



@app.get("/hello")
def hello():
    return {"message": "Hello from VidTalk!"}


