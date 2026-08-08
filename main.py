from fastapi import FastAPI, HTTPException

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
