# Task API

A simple REST API built with **Python and FastAPI** for managing tasks.

This project was built as part of the FlyRank Backend Internship Track and covers the fundamentals of building a CRUD API, including creating, reading, updating, and deleting tasks.

## Features

- Create a new task
- Get all tasks
- Get a single task by ID
- Update a task
- Delete a task
- Input validation
- Appropriate HTTP status codes
- Interactive Swagger API documentation

## Tech Stack

- Python
- FastAPI
- Uvicorn

## Installation & Running

### 1. Clone the repository

```bash
git clone https://github.com/NamraAjmal/backend.git
cd backend
```

### 2. Install dependencies

```bash
pip install fastapi uvicorn
```

### 3. Run the server

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Swagger UI is available at:

```text
http://localhost:8000/docs
```

## API Endpoints

| Method | Endpoint      | Description                          | Success         |
| ------ | ------------- | ------------------------------------ | --------------- |
| GET    | `/`           | Returns basic API information        | 200             |
| GET    | `/health`     | Checks whether the server is running | 200             |
| GET    | `/tasks`      | Returns all tasks                    | 200             |
| GET    | `/tasks/{id}` | Returns a task by ID                 | 200 / 404       |
| POST   | `/tasks`      | Creates a new task                   | 201             |
| PUT    | `/tasks/{id}` | Updates a task                       | 200 / 400 / 404 |
| DELETE | `/tasks/{id}` | Deletes a task                       | 204 / 404       |

## Example Request

Create a task:

```bash
curl -i -X POST http://localhost:8000/tasks \
-H "Content-Type: application/json" \
-d '{"title":"Learn FastAPI"}'
```

Example output:

```text
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Learn FastAPI","done":false}
```

## Swagger UI

FastAPI automatically generates interactive API documentation using OpenAPI and Swagger UI.

Open:

```text
http://localhost:8000/docs
```

Use the **Try it out** button to create, read, update, and delete tasks directly from the browser.

### Swagger Screenshot

![Swagger UI](Screenshot_11-8-2026_18146_127.0.0.1.jpeg)

## Project Structure

```text
.
├── main.py
├── README.md
```

## Status Codes

The API uses HTTP status codes to communicate the result of each request:

- `200` — Request successful
- `201` — Task successfully created
- `204` — Task successfully deleted
- `400` — Invalid or empty request
- `404` — Task not found

## Project Status

Complete CRUD API with interactive Swagger documentation.
