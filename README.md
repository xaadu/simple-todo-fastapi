# Simple Todo API

A simple, RESTful Todo API built with FastAPI and SQLite3.

## Features

- Create, read, update, and delete todo items
- Filter todos by completion status
- Automatic Swagger documentation at `/docs`

## Requirements

- Python 3.13 or later
- FastAPI
- Uvicorn
- Other dependencies listed in `requirements.txt`

## Installation

1. Clone this repository:

```bash
git clone https://github.com/xaadu/simple-todo-fastapi.git
cd simple-todo-fastapi
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Unix/macOS
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the server with:

```bash
uvicorn app:app
```

The API will be available at: http://127.0.0.1:8000

## API Documentation

Once the application is running, visit:

- Interactive API documentation (Swagger): http://127.0.0.1:8000/docs
- Alternative API documentation (ReDoc): http://127.0.0.1:8000/redoc

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Welcome message |
| POST | `/todos/` | Create a new todo |
| GET | `/todos/` | List all todos |
| GET | `/todos/{todo_id}` | Get a specific todo |
| PUT | `/todos/{todo_id}` | Update a specific todo |
| DELETE | `/todos/{todo_id}` | Delete a specific todo |
| GET | `/todos/completed/` | List all completed todos |
| GET | `/todos/pending/` | List all pending (not completed) todos |

## Example Usage

### Create a Todo

```bash
curl -X POST "http://127.0.0.1:8000/todos/" -H "Content-Type: application/json" -d '{"title": "Learn FastAPI", "description": "Complete the FastAPI tutorial"}'
```

### Get All Todos

```bash
curl -X GET "http://127.0.0.1:8000/todos/"
```

### Mark a Todo as Completed

```bash
curl -X PUT "http://127.0.0.1:8000/todos/{todo_id}" -H "Content-Type: application/json" -d '{"completed": true}'
```

## Credit

This project is created and maintained by [xaadu](https://zayedabdullah.com).
