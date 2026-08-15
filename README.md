# Task API

A simple REST API built with **Python**, **FastAPI**, and **SQLite** for managing tasks.

This project was built as part of the FlyRank Backend Internship Track and demonstrates a complete CRUD API with persistent database storage.

## Features

- Create a new task
- Get all tasks
- Get a single task by ID
- Update a task
- Delete a task
- SQLite database persistence
- Automatic database initialization and seeding
- Input validation
- Appropriate HTTP status codes
- Interactive Swagger API documentation

## Tech Stack

- Python
- FastAPI
- SQLite
- Uvicorn

## Why SQLite?

SQLite was chosen because:

- It stores data in a single file (`tasks.db`)
- It requires zero server setup
- It is lightweight and easy to use
- Data survives application restarts
- Perfect for small projects and learning backend development

## Database

The application uses a SQLite database stored in:

```text
tasks.db
```

The database file is created automatically when the application starts if it does not already exist.

On first startup, the application:

1. Creates the `tasks` table
2. Seeds three example tasks
3. Starts serving requests immediately

This means a new user can clone the repository and run the project without any manual database setup.

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

### 3. Start the server

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

Example response:

```json
{
  "id": 4,
  "title": "Learn FastAPI",
  "done": false
}
```

## Exploring SQLite

Example query used during database exploration:

```sql
SELECT * FROM tasks;
```

Result:

This query returned all tasks currently stored in the database.

### SQLite Screenshot

![SQLite Query](image.png)

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
├── tasks.db (generated automatically at runtime)
```

## Status Codes

The API uses HTTP status codes to communicate request results:

- `200` — Request successful
- `201` — Task successfully created
- `204` — Task successfully deleted
- `400` — Invalid request
- `404` — Task not found

## Project Status

Complete CRUD API
SQLite database integration
Automatic database initialization
Persistent storage across restarts
Interactive Swagger documentation
