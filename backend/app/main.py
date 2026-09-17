from app.routes.users import router as users_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(users_router)



@app.get("/hello")
def hello():
    return {"message": "Hello from VidTalk!"}




