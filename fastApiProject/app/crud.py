import redis
from app.models import Task
from pydantic import json


# from app.routers import tasks_router

def create_task(redis_client: redis.Redis, task: Task):
    redis_key = f"task:{task.id}"
    redis_client.set(redis_key, task.json())
    return task


def get_task_by_id(redis_client: redis.Redis, task_id: int):
    redis_key = f"task:{task_id}"
    task_json = redis_client.get(redis_key)
    if task_json is None:
        return None
    task_data = json.loads(task_json)
    return Task(**task_data)


def update_task(redis_client: redis.Redis, task_id: int, task: Task):
    redis_key = f"task:{task_id}"
    if not redis_client.exists(redis_key):
        return None
    redis_client.set(redis_key, task.json())
    return task


def delete_task(redis_client: redis.Redis, task_id: int):
    redis_key = f"task:{task_id}"
    if not redis_client.exists(redis_key):
        return False
    redis_client.delete(redis_key)
    return True
