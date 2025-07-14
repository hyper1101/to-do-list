# 📝 To-Do List API (FastAPI + PostgreSQL + Docker)

This is a backend REST API built with **FastAPI**, connected to a **PostgreSQL** database, and containerized using **Docker**. The API supports user authentication and task management features including creation, update, filtering, sorting, and statistics.

---

## 🚀 Features

- 🔐 JWT-based authentication  
- 👤 User registration & login  
- ✅ CRUD operations on to-do tasks  
- 📅 Due dates with overdue detection  
- 🔍 Filtering by completion status  
- 📊 Per-user task statistics  
- 🐳 Dockerized setup

---

## 🛠️ Tech Stack

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Passlib (for password hashing)
- Docker & Docker Compose

---

## 📁 Project Structure

├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   ├── auth.py
│   │   └── database.py
│   └── Dockerfile
├── docker-compose.yml


## 🐳 Getting Started with Docker

### 1. Clone the repo

```bash
git clone https://github.com/your-username/todo-backend.git
cd todo-backend
````

### 2. Start the containers

```bash
docker-compose up --build
```

### 3. Access the API

* FastAPI Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)
* Backend base URL: `http://localhost:8000`

---

## ⚙️ Environment Variables

Make sure your `docker-compose.yml` includes:

```yaml
environment:
  POSTGRES_USER: user
  POSTGRES_PASSWORD: password
  POSTGRES_DB: todos
```

And your FastAPI app loads this database URL:

```
DATABASE_URL=postgresql://user:password@db/todos
```

---

## 🔐 Authentication Flow

* `POST /users/` → Register new users
* `POST /token` → Get JWT access token
* Use the token in headers:

```
Authorization: Bearer <your_token>
```

---

## 📌 API Endpoints

| Method | Endpoint         | Description                        |
| ------ | ---------------- | ---------------------------------- |
| POST   | `/users/`        | Register a new user                |
| POST   | `/token`         | Login and get JWT token            |
| GET    | `/todos/`        | List user’s to-dos (auth required) |
| POST   | `/todos/`        | Create a new task                  |
| PUT    | `/todos/{id}`    | Update a task                      |
| DELETE | `/todos/{id}`    | Delete a task                      |
| GET    | `/todos/stats`   | Get task stats per user            |
| GET    | `/todos/overdue` | List overdue tasks                 |

---

## ✅ Example Request (with `curl`)

```bash
curl -X POST http://localhost:8000/token \
  -d "username=john&password=secret" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

---

## 🧪 How to Run (Recap)

```bash
# Step 1: Navigate to the project folder
cd /path/to/todo-backend

# Step 2: Run the whole app
docker-compose up --build

# Step 3: Open your browser
http://localhost:8000/docs
```
