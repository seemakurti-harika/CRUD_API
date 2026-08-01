import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()
# Connect to SQLite database
conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()
# Create tasks table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL
)
""")

conn.commit()
# Check if the table is empty
cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]

# Seed initial tasks only if the table is empty
if count == 0:
    sample_tasks = [
        ("Learn FastAPI", False),
        ("Complete Assignment", False),
        ("Watch Movie", True)
    ]

    cursor.executemany(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        sample_tasks
    )

    conn.commit()
class TaskCreate(BaseModel):
    title: str
class TaskUpdate(BaseModel):
    title: str
    done: bool
@app.get("/")
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }
@app.get("/tasks")
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    tasks = []

    for row in rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "done": bool(row[2])
        })

    return tasks
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    # Validate title
    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    # Insert into database
    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task.title, False)
    )

    conn.commit()

    # Get the ID of the newly inserted row
    task_id = cursor.lastrowid

    return {
        "id": task_id,
        "title": task.title,
        "done": False
    }
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    row = cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "id": row[0],
        "title": row[1],
        "done": bool(row[2])
    }
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    row = cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    cursor.execute(
        """
        UPDATE tasks
        SET title = ?, done = ?
        WHERE id = ?
        """,
        (updated_task.title, updated_task.done, task_id)
    )

    conn.commit()

    return {
        "id": task_id,
        "title": updated_task.title,
        "done": updated_task.done
    }
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    row = cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()

    return {
        "message": "Task deleted successfully"
    }
