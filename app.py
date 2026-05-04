import uuid
from datetime import datetime, UTC
from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="Task Management API")

app.config = {}


tasks = {}


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


@app.get("/tasks")
async def get_tasks():
    return list(tasks.values())


@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    task = tasks.get(task_id)

    if not task:
        raise HTTPException(status_code=404, detail={"error": "Task not found"})

    return task


@app.post("/tasks", status_code=201)
async def create_task(task_data: TaskCreate):
    task_id = str(uuid.uuid4())

    task = {
        "id": task_id,
        "title": task_data.title,
        "description": task_data.description,
        "completed": False,
        "created_at": datetime.now(UTC).isoformat(),
    }

    tasks[task_id] = task
    return task


@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task_data: TaskUpdate):
    task = tasks.get(task_id)

    if not task:
        raise HTTPException(status_code=404, detail={"error": "Task not found"})

    update_data = task_data.model_dump(exclude_unset=True)

    if "title" in update_data:
        task["title"] = update_data["title"]

    if "description" in update_data:
        task["description"] = update_data["description"]

    if "completed" in update_data:
        task["completed"] = update_data["completed"]

    task["updated_at"] = datetime.now(UTC).isoformat()
    tasks[task_id] = task

    return task


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    task = tasks.get(task_id)

    if not task:
        raise HTTPException(status_code=404, detail={"error": "Task not found"})

    del tasks[task_id]
    return {"message": "Task deleted successfully"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)