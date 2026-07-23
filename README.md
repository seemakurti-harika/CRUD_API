# CRUD API with FastAPI

A simple Task Management REST API built using FastAPI as part of the FlyRank Internship Backend Track Week 2 Assignment.

## Features

- Get all tasks
- Get a task by ID
- Create a new task
- Update an existing task
- Delete a task

## Technologies Used

- Python
- FastAPI
- Uvicorn

## Installation

1. Clone the repository

```bash
git clone https://github.com/seemakurti-harika/CRUD_API.git
```

2. Move into the project folder

```bash
cd CRUD_API
```

3. Create a virtual environment

```bash
python -m venv venv
```

4. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

5. Install dependencies

```bash
pip install fastapi uvicorn
```

## Run the application

```bash
uvicorn main:app --reload
```

The API will run at:

```
http://127.0.0.1:8000
```

Swagger UI:

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
| POST | /tasks | Create task |
| PUT | /tasks/{id} | Update task |
| DELETE | /tasks/{id} | Delete task |

## Author

Harika
