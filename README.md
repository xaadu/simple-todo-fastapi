# 📋 Simple Todo API

A friendly, easy-to-use Todo API built with FastAPI and SQLite3. Perfect for learning RESTful API concepts or as a starter for your own projects!

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

## ✨ Features

- ✅ Create, read, update, and delete todo items
- 🔍 Filter todos by completion status
- 📚 Beautiful API documentation with Swagger UI at `/docs`
- 🚀 Fast and lightweight with SQLite database
- 🛠️ Easy setup and installation

## 📋 Requirements

- Python 3.13 or later
- All other dependencies will be installed from `requirements.txt`

## 🚀 Quick Start

### Installation

1. **Clone this repository:**

   ```bash
   git clone https://github.com/xaadu/simple-todo-fastapi.git
   cd simple-todo-fastapi
   ```

2. **Set up a virtual environment:**

   ```bash
   # Create the virtual environment
   python -m venv venv
   
   # Activate it on Windows
   venv\Scripts\activate
   
   # Or activate it on macOS/Linux
   # source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the server with:

```bash
uvicorn app:app --reload
```

The `--reload` flag enables auto-reloading when you make code changes (great for development).

📱 Your API will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 📚 API Documentation

Once the application is running, you can explore and test the API:

- 🔍 **Interactive API documentation (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- 📖 **Alternative documentation (ReDoc)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🛣️ API Endpoints

| Method | URL | Description |
|:------:|-----|-------------|
| GET | `/` | Welcome message |
| POST | `/todos/` | Create a new todo |
| GET | `/todos/` | List all todos |
| GET | `/todos/{todo_id}` | Get a specific todo |
| PUT | `/todos/{todo_id}` | Update a specific todo |
| DELETE | `/todos/{todo_id}` | Delete a specific todo |
| GET | `/todos/completed/` | List all completed todos |
| GET | `/todos/pending/` | List all pending todos |

## 💡 Example Usage

### Using the Swagger UI (Recommended)

The easiest way to interact with the API is through the Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Using cURL

#### Create a Todo

```bash
curl -X POST "http://127.0.0.1:8000/todos/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI", "description": "Complete the FastAPI tutorial"}'
```

#### Get All Todos

```bash
curl -X GET "http://127.0.0.1:8000/todos/"
```

#### Mark a Todo as Completed

```bash
curl -X PUT "http://127.0.0.1:8000/todos/{todo_id}" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

## 👨‍💻 Credit

This project is created and maintained by [xaadu](https://zayedabdullah.com).

---

⭐ If you find this project helpful, please consider giving it a star on GitHub!
