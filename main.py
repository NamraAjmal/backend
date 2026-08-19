from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response
import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


app = FastAPI()


@app.get("/", description="Basic Information")
async def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", description="Status check")
async def health():
    return {"status": "ok"}


@app.get("/tasks", description="Returns all tasks")
async def tasks():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks")
            rows = cur.fetchall()
    task_list = []
    for row in rows:
        task = {"id": row[0], "title": row[1], "done": bool(row[2])}
        task_list.append(task)
    return task_list


@app.get("/tasks/{id}", description="Returns task by ID")
async def task(id: int):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks WHERE id=%s", (id,))
            row = cur.fetchone()
    if row:
        task = {"id": row[0], "title": row[1], "done": bool(row[2])}
        return task
    else:
        return JSONResponse(status_code=404, content={"error": "Task not found"})


@app.post("/tasks", description="Adds a task")
async def create_task(task: dict):
    if "title" not in task or task["title"] == "":
        raise HTTPException(status_code=400, detail="Title does not exist")

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tasks (title,done) VALUES (%s,%s) RETURNING *",
                (task["title"], False),
            )
            row = cur.fetchone()
            conn.commit()
    new_task = {"id": row[0], "title": row[1], "done": row[2]}
    return JSONResponse(status_code=201, content=new_task)


@app.put("/tasks/{id}", description="Updates task by ID")
async def update_task(id: int, updatedtask: dict):
    if not updatedtask:
        return JSONResponse(status_code=400, content={"error": "Empty request"})
    if "title" not in updatedtask and "done" not in updatedtask:
        return JSONResponse(status_code=400, content={"error": "Invalid request"})
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks WHERE id=%s", (id,))
            row = cur.fetchone()
    if row is None:
        return JSONResponse(status_code=404, content={"error": "Task does not exist"})
    new_title = row[1]
    new_done = row[2]
    if "title" in updatedtask:
        if updatedtask["title"] == "":
            return JSONResponse(status_code=400, content="Title can't be empty")
        new_title = updatedtask["title"]
    if "done" in updatedtask:
        if not isinstance(updatedtask["done"], bool):
            return JSONResponse(
                status_code=400, content="Done can only be a boolean value"
            )
        new_done = updatedtask["done"]
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE tasks SET title=%s, done=%s WHERE id=%s",
                (new_title, new_done, id),
            )
        conn.commit()
    new_task = {"id": id, "title": new_title, "done": new_done}
    return JSONResponse(status_code=200, content=new_task)


@app.delete("/tasks/{id}", description="Deletes a task")
async def delete_task(id: int):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks WHERE id=%s", (id,))
            row = cur.fetchone()
    if row is None:
        return JSONResponse(status_code=404, content="Task does not exist")
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tasks where id=%s", (id,))
        conn.commit()
    return Response(status_code=204)
