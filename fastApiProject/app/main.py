from fastapi import FastAPI
import uvicorn

from app.database import Base, engine
from app.routers import tasks_router, auth_router
from app.dependencies import create_redis_client
import threading

app = FastAPI()

Base.metadata.create_all(bind=engine)
redis_client = create_redis_client()

app.include_router(tasks_router)
app.include_router(auth_router)


@app.get("/")
def read_root():
    return {"Hello World"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
