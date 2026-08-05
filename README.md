# Todo API with FastAPI, PostgreSQL & Supabase Authentication

A secure REST API built using **FastAPI**, **PostgreSQL**, and **Supabase Authentication** as part of the FlyRank Internship Backend Track.

## Features

### Authentication
- User Signup
- User Login
- JWT Authentication using Supabase
- Protected Routes

### Todo Management
- Create Todo
- Get All Todos
- Get Todo by ID
- Update Todo
- Delete Todo
- User-specific Todos (each user can access only their own data)

## Technologies Used

- Python 3
- FastAPI
- PostgreSQL
- Supabase Authentication
- Psycopg2
- Pydantic
- Uvicorn
- Python-dotenv
- Docker

---

## Project Structure

```
CRUD_API/
│
├── main.py
├── requirements.txt
├── .env.example
├── Dockerfile
├── compose.yaml
├── README.md
└── .gitignore
```

---

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

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

Example:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=taskdb
DB_USER=postgres
DB_PASSWORD=password

SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

---

## Run the Application

```bash
python -m uvicorn main:app --reload
```

API:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

---

## Authentication Flow

1. Register a user using:

```
POST /auth/signup
```

2. Login using:

```
POST /auth/login
```

3. Copy the **access_token** returned after login.

4. Click **Authorize** in Swagger and paste the access token.

5. Access protected endpoints.

---

## API Endpoints

### Public

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Home |
| GET | /health | Health Check |
| GET | /public/info | Public Endpoint |
| GET | /supabase-test | Test Supabase Connection |

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/signup | Register User |
| POST | /auth/login | Login User |

### Protected

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /protected/profile | Get Logged-in User |

### Todo API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /todos | Create Todo |
| GET | /todos | Get All Todos |
| GET | /todos/{id} | Get Todo by ID |
| PUT | /todos/{id} | Update Todo |
| DELETE | /todos/{id} | Delete Todo |

---

## Docker

Build and start the containers:

```bash
docker compose up --build
```

Stop the containers:

```bash
docker compose down
```

---

## Author

**Seemakurti Harika**

GitHub:
https://github.com/seemakurti-harika

---

## License

This project was developed for the **FlyRank Backend Internship**.
