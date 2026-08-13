from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response
import sqlite3

app = FastAPI()


def initialize_database():
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS tasks(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        done INTEGER NOT NULL)""")
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute("INSERT INTO tasks (title,done) VALUES (?,?)", ("Buy Milk", 0))
        cursor.execute("INSERT INTO tasks (title,done) VALUES (?,?)", ("Pray", 1))
        cursor.execute("INSERT INTO tasks (title,done) VALUES (?,?)", ("Exercise", 0))
        connection.commit()
    connection.close()


initialize_database()


taskList = [
    {"id": 1, "title": "Buy Milk", "done": False},
    {"id": 2, "title": "Attend meeting", "done": True},
    {"id": 3, "title": "Pray", "done": True},
]


@app.get("/", description="Basic Information")
async def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", description="Status check")
async def health():
    return {"status": "ok"}


@app.get("/tasks", description="Returns all tasks")
async def tasks():
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    connection.close()
    task_list = []
    for row in rows:
        task = {"id": row[0], "title": row[1], "done": bool(row[2])}
        task_list.append(task)
    return task_list


@app.get("/tasks/{id}", description="Returns task by ID")
async def task(id: int):
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id= ?", (id,))
    row = cursor.fetchone()
    connection.close()
    if row:
        task = {"id": row[0], "title": row[1], "done": bool(row[2])}
        return task
    else:
        raise HTTPException(status_code=404, detail="Task " + str(id) + " not found")


@app.post("/tasks", description="Adds a task")
async def create_task(task: dict):
    if "title" not in task or task["title"] == "":
        raise HTTPException(status_code=400, detail="Title does not exist")

    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO tasks (title,done) VALUES (?,?)", (task["title"], 0))
    connection.commit()
    new_task = {"id": cursor.lastrowid, "title": task["title"], "done": False}
    connection.close()
    return JSONResponse(status_code=201, content=new_task)


@app.put("/tasks/{id}", description="Updates task by ID")
async def update_task(id: int, updatedtask: dict):
    if not updatedtask:
        return JSONResponse(status_code=400, content={"error": "Empty request"})
    if "title" not in updatedtask and "done" not in updatedtask:
        return JSONResponse(status_code=400, content={"error": "Invalid request"})
    for task in taskList:
        if task["id"] == id:
            if "title" in updatedtask:
                if updatedtask["title"] == "":
                    return JSONResponse(status_code=400, content="Title can't be empty")
                task["title"] = updatedtask["title"]
            if "done" in updatedtask:
                if not isinstance(updatedtask["done"], bool):
                    return JSONResponse(status_code=400, content="Invalid request")
                task["done"] = updatedtask["done"]
            return JSONResponse(status_code=200, content=task)
    return JSONResponse(status_code=404, content="Task does not exist")


@app.delete("/tasks/{id}", description="Deletes a task")
async def delete_task(id: int):
    for task in taskList:
        if task["id"] == id:
            taskList.remove(task)
            return Response(status_code=204)
    return JSONResponse(status_code=404, content="Task does not exist")
