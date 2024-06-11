from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import redis

router = APIRouter()

redis_client = redis.Redis(host='localhost', port=6379, db=0)


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str
    due_date: str


@router.post("/tasks/")
async def create_task(task: Task):
    redis_key = f"task:{task.id}"
    redis_client.set(redis_key, task.json())
    return task


@router.put("/tasks/{task_id}")
async def update_task(task_id: int, task: Task):
    redis_key = f"task:{task_id}"
    if not redis_client.exists(redis_key):
        raise HTTPException(status_code=404, detail=f"Zadatak sa id brojem {task_id} nije pronadđen")
    redis_client.set(redis_key, task.json())
    return task


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    redis_key = f"task:{task_id}"
    if not redis_client.exists(redis_key):
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    redis_client.delete(redis_key)
    return {"message": f"Zadatak {task_id} uspješno izbrisan"}


@router.get("/tasks/{task_id}", response_model=Task)
async def get_task_by_id(task_id: int):
    redis_key = f"task:{task_id}"
    task_json = redis_client.get(redis_key)
    if task_json is None:
        raise HTTPException(status_code=404, detail=f"Zadatak sa id brojem {task_id} nije pronadđen")
    try:
        task_data = json.loads(task_json)
        return Task(**task_data)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Error decoding task data: {e}")
