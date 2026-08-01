# CRUD API with FastAPI & SQLite

A Task Management REST API built using **FastAPI** and **SQLite** as part of the **FlyRank Internship Backend Track – Week 3 Assignment**.

## Project Description

This project implements a CRUD (Create, Read, Update, Delete) API for managing tasks.

Initially, tasks were stored in an in-memory list. In Week 3, the application was migrated to **SQLite**, allowing task data to persist even after restarting the server.

## Features

- Get all tasks
- Get a task by ID
- Create a new task
- Update an existing task
- Delete a task
- Automatic SQLite database creation
- Automatic table creation
- Automatic seeding of sample tasks on first run
- Persistent storage using SQLite

## Technologies Used

- Python
- FastAPI
- SQLite
- Uvicorn

## Why SQLite?

SQLite is a lightweight relational database that stores data in a single file (`tasks.db`). It requires no separate database server, making it ideal for small applications and learning backend development. It also ensures that task data persists after the server restarts.

## Database

Database file:

```
tasks.db
```

The application automatically:

- Creates the database if it doesn't exist.
- Creates the `tasks` table if it doesn't exist.
- Inserts three sample tasks only on the first run.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/seemakurti-harika/CRUD_API.git
```

### 2. Navigate to the project

```bash
cd CRUD_API
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install fastapi uvicorn
```

## Run the Application

```bash
python -m uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Home |
| GET | /health | Health Check |
| GET | /tasks | Get all tasks |
| GET | /tasks/{id} | Get task by ID |
| POST | /tasks | Create a new task |
| PUT | /tasks/{id} | Update a task |
| DELETE | /tasks/{id} | Delete a task |

## Example SQL Query

```sql
SELECT * FROM tasks;
```

This query retrieves all tasks stored in the SQLite database.

## Database Screenshot

Add a screenshot of the `tasks` table from **DB Browser for SQLite** here.

Example:

```
images/database.png
```

```markdown
![Database Screenshot](images/database.png)
```

## Project Structure

```
CRUD_API/
│── main.py
│── tasks.db
│── README.md
│── .gitignore
└── requirements.txt
```

## Author

**Seemakurti Harika**
