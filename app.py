import uuid
from datetime import datetime, UTC
from typing import Optional

import uvicorn
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI(title="Task Management API")
app.config = {}


# --- Flask compatibility layer ---
class FlaskLikeResponse:
    def __init__(self, response):
        self.status_code = response.status_code
        self.data = response.content


class FlaskLikeClient:
    def __init__(self, app):
        self.client = TestClient(app)

    def get(self, url):
        return FlaskLikeResponse(self.client.get(url))

    def post(self, url, json=None, content_type=None):
        return FlaskLikeResponse(self.client.post(url, json=json))

    def put(self, url, json=None, content_type=None):
        return FlaskLikeResponse(self.client.put(url, json=json))

    def delete(self, url):
        return FlaskLikeResponse(self.client.delete(url))

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


def test_client():
    return FlaskLikeClient(app)


app.test_client = test_client


# --- Storage ---
tasks = {}


# --- Models ---
class TaskCreate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = ""


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


# --- Routes ---
@app.get("/tasks")
async def get_tasks():
    return JSONResponse(list(tasks.values()), status_code=200)


@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    task = tasks.get(task_id)
    if not task:
        return JSONResponse({"error": "Task not found"}, status_code=404)
    return JSONResponse(task, status_code=200)


@app.post("/tasks")
async def create_task(request: Request):
    data = await request.json() if request.headers.get("content-type") else None

    if not data or "title" not in data:
        return JSONResponse({"error": "Title is required"}, status_code=400)

    task_id = str(uuid.uuid4())

    task = {
        "id": task_id,
        "title": data["title"],
        "description": data.get("description", ""),
        "completed": False,
        "created_at": datetime.now(UTC).isoformat(),
    }

    tasks[task_id] = task
    return JSONResponse(task, status_code=201)


@app.put("/tasks/{task_id}")
async def update_task(task_id: str, request: Request):
    task = tasks.get(task_id)
    if not task:
        return JSONResponse({"error": "Task not found"}, status_code=404)

    data = await request.json() if request.headers.get("content-type") else None
    if not data:
        return JSONResponse({"error": "No data provided"}, status_code=400)

    if "title" in data:
        task["title"] = data["title"]
    if "description" in data:
        task["description"] = data["description"]
    if "completed" in data:
        task["completed"] = data["completed"]

    task["updated_at"] = datetime.now(UTC).isoformat()
    return JSONResponse(task, status_code=200)


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    task = tasks.get(task_id)
    if not task:
        return JSONResponse({"error": "Task not found"}, status_code=404)

    del tasks[task_id]
    return JSONResponse({"message": "Task deleted successfully"}, status_code=200)


@app.get("/health")
async def health():
    return JSONResponse({"status": "healthy"}, status_code=200)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)