from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from datetime import datetime
from contextlib import contextmanager, asynccontextmanager
import os
import uuid

# Database setup
DB_PATH = "todos.db"


def init_db():
    """Initialize database with todo table if it doesn't exist"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS todos (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        )
        conn.commit()


@contextmanager
def get_db():
    """Database connection context manager"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    try:
        yield conn
    finally:
        conn.close()


# Pydantic models
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class Todo(TodoBase):
    id: str
    created_at: str
    updated_at: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1c52b386-4ac7-4d3d-b9ea-0ac293bcda7a",
                "title": "Complete project",
                "description": "Finish the FastAPI todo project",
                "completed": False,
                "created_at": "2025-05-11T10:00:00",
                "updated_at": "2025-05-11T10:00:00",
            }
        }


# Initialize database through lifespan context manager
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database on startup
    init_db()
    yield
    # Cleanup operations can go here (if any)


# Create app instance
app = FastAPI(
    title="Simple Todo API",
    description="A simple Todo API built with FastAPI and SQLite3",
    version="1.0.0",
    lifespan=lifespan,
)


# Routes
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Todo API! Go to /docs for documentation."}


@app.post(
    "/todos/", response_model=Todo, status_code=status.HTTP_201_CREATED, tags=["Todos"]
)
def create_todo(todo: TodoCreate):
    """Create a new todo item"""
    with get_db() as conn:
        cursor = conn.cursor()
        todo_id = str(uuid.uuid4())
        now = datetime.now().isoformat()

        cursor.execute(
            "INSERT INTO todos (id, title, description, completed, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
            (todo_id, todo.title, todo.description, todo.completed, now, now),
        )
        conn.commit()

        # Retrieve the created todo
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()

        return dict(row)


@app.get("/todos/", response_model=List[Todo], tags=["Todos"])
def read_todos():
    """Get all todo items"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


@app.get("/todos/{todo_id}", response_model=Todo, tags=["Todos"])
def read_todo(todo_id: str):
    """Get a specific todo item by ID"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()

        if row is None:
            raise HTTPException(status_code=404, detail="Todo not found")

        return dict(row)


@app.put("/todos/{todo_id}", response_model=Todo, tags=["Todos"])
def update_todo(todo_id: str, todo: TodoUpdate):
    """Update a todo item"""
    with get_db() as conn:
        cursor = conn.cursor()
        # First check if todo exists
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        existing = cursor.fetchone()

        if existing is None:
            raise HTTPException(status_code=404, detail="Todo not found")

        # Update only the fields that are provided
        existing_dict = dict(existing)
        update_data = todo.model_dump(exclude_unset=True)

        # Don't update if no fields are provided
        if not update_data:
            return existing_dict

        # Prepare SQL for updating only specified fields
        fields = []
        values = []

        for field, value in update_data.items():
            fields.append(f"{field} = ?")
            values.append(value)

        # Always update the updated_at field
        fields.append("updated_at = ?")
        values.append(datetime.now().isoformat())

        # Add the todo_id for the WHERE clause
        values.append(todo_id)

        # Execute the update
        cursor.execute(
            f"UPDATE todos SET {', '.join(fields)} WHERE id = ?", tuple(values)
        )
        conn.commit()

        # Retrieve the updated todo
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()

        return dict(row)


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Todos"])
def delete_todo(todo_id: str):
    """Delete a todo item"""
    with get_db() as conn:
        cursor = conn.cursor()
        # First check if todo exists
        cursor.execute("SELECT id FROM todos WHERE id = ?", (todo_id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Todo not found")

        # Delete the todo
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()

        return None  # 204 No Content


@app.get("/todos/completed/", response_model=List[Todo], tags=["Todos"])
def read_completed_todos():
    """Get all completed todo items"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM todos WHERE completed = TRUE ORDER BY updated_at DESC"
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


@app.get("/todos/pending/", response_model=List[Todo], tags=["Todos"])
def read_pending_todos():
    """Get all pending todo items"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM todos WHERE completed = FALSE ORDER BY created_at DESC"
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


# Run with: uvicorn app:app --reload
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
