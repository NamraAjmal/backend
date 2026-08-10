from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response

app = FastAPI()

taskList = [
    {"id": 1, "title": "Buy Milk", "done": False},
    {"id": 2, "title": "Attend meeting", "done": True},
    {"id": 3, "title": "Pray", "done": True},
]


@app.get("/")
async def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/tasks")
async def tasks():
    if taskList:
        return taskList


@app.get("/tasks/{id}")
async def task(id: int):
    for task in taskList:
        if task["id"] == id:
            return task
    else:
        raise HTTPException(status_code=404, detail="Task " + str(id) + " not found")


@app.post("/tasks")
async def create_task(task: dict):
    if "title" not in task or task["title"] == "":
        raise HTTPException(status_code=400, detail="Title does not exist")

    new_task = {
        "id": max(task["id"] for task in taskList) + 1,
        "title": task["title"],
        "done": False,
    }
    taskList.append(new_task)
    return JSONResponse(status_code=201, content=new_task)


@app.put("/tasks/{id}")
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


@app.delete("/tasks/{id}")
async def delete_task(id: int):
    for task in taskList:
        if task["id"] == id:
            taskList.remove(task)
            return Response(status_code=204)
    return JSONResponse(status_code=404, content="Task does not exist")
