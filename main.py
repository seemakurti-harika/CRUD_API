from dotenv import load_dotenv
from supabase import create_client, Client
import psycopg2
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
app = FastAPI()
security = HTTPBearer()
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        response = supabase.auth.get_user(token)
        return response.user
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    user_id UUID NOT NULL
)
""")

conn.commit()
class UserSignup(BaseModel):
    email: str
    password: str
class TaskCreate(BaseModel):
    title: str
class TaskUpdate(BaseModel):
    title: str
    done: bool
class UserLogin(BaseModel):
    email: str
    password: str
class TodoCreate(BaseModel):
    title: str


class TodoUpdate(BaseModel):
    title: str
    completed: bool
@app.get("/")
def home():
    return {
        "name": "Task API",
        "version": "1.0"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/supabase-test")
def supabase_test():
    return {
        "message": "Supabase connected successfully!"
    }
@app.post("/auth/signup")
def signup(user: UserSignup):
    try:
        response = supabase.auth.sign_up(
            {
                "email": user.email,
                "password": user.password,
            }
        )

        return {
            "user": response.user.model_dump() if response.user else None,
            "session": response.session.model_dump() if response.session else None
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@app.post("/auth/login")
def login(user: UserLogin):
    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": user.email,
                "password": user.password,
            }
        )

        return {
            "message": "Login successful",
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "user": response.user.email
        }

    except Exception as e:
        raise HTTPException(
        status_code=401,
        detail=str(e)
    )
@app.get("/public/info")
def public_info():
    return {
        "message": "This is a public endpoint."
    }
@app.get("/protected/profile")
def protected_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        user = supabase.auth.get_user(token)

        return {
            "message": "Protected route accessed successfully",
            "email": user.user.email
        }

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
@app.post("/todos")
def create_todo(
    todo: TodoCreate,
    user=Depends(get_current_user)
):
    cursor.execute(
        """
        INSERT INTO todos(title, completed, user_id)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (todo.title, False, user.id)
    )

    todo_id = cursor.fetchone()[0]
    conn.commit()

    return {
        "id": todo_id,
        "title": todo.title,
        "completed": False
    }
@app.get("/todos")
def get_todos(user=Depends(get_current_user)):
    cursor.execute(
        """
        SELECT id, title, completed
        FROM todos
        WHERE user_id = %s
        ORDER BY id
        """,
        (user.id,)
    )

    rows = cursor.fetchall()

    todos = []

    for row in rows:
        todos.append({
            "id": row[0],
            "title": row[1],
            "completed": row[2]
        })

    return todos
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int, user=Depends(get_current_user)):

    cursor.execute(
        """
        SELECT id, title, completed
        FROM todos
        WHERE id = %s
        AND user_id = %s
        """,
        (todo_id, user.id)
    )

    row = cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    return {
        "id": row[0],
        "title": row[1],
        "completed": row[2]
    }
@app.put("/todos/{todo_id}")
def update_todo(
    todo_id: int,
    todo: TodoUpdate,
    user=Depends(get_current_user)
):

    cursor.execute(
        """
        SELECT id
        FROM todos
        WHERE id = %s
        AND user_id = %s
        """,
        (todo_id, user.id)
    )

    if cursor.fetchone() is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    cursor.execute(
        """
        UPDATE todos
        SET title = %s,
            completed = %s
        WHERE id = %s
        """,
        (todo.title, todo.completed, todo_id)
    )

    conn.commit()

    return {
        "message": "Todo updated successfully"
    }
@app.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    user=Depends(get_current_user)
):

    cursor.execute(
        """
        SELECT id
        FROM todos
        WHERE id = %s
        AND user_id = %s
        """,
        (todo_id, user.id)
    )

    if cursor.fetchone() is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    cursor.execute(
        "DELETE FROM todos WHERE id = %s",
        (todo_id,)
    )

    conn.commit()

    return {
        "message": "Todo deleted successfully"
    }