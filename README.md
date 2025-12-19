# 📘 Blog RESTful API

A RESTful API built using **FastAPI** and **Peewee ORM** to manage authors and their blog posts.  
This project demonstrates how to design and implement a **one-to-many relationship** between data entities with proper validation, cascade deletes, and efficient queries.

---

## 🚀 Objective

To build a backend API for a simple blog platform that:
- Manages **Authors** and their **Posts**
- Enforces database relationships using foreign keys
- Handles cascading deletes
- Avoids N+1 query problems
- Serves related data efficiently

---

## ✨ Features

- CRUD operations for **Authors** and **Posts**
- One-to-many relationship (One Author → Many Posts)
- Foreign key constraint with **ON DELETE CASCADE**
- Validation for non-existent authors when creating posts
- Nested endpoint to fetch posts for a specific author
- Efficient JOIN queries to avoid N+1 problem
- Interactive API documentation using Swagger UI

---

## 🛠 Tech Stack

- **FastAPI** – Web framework
- **Peewee ORM** – ORM for database operations
- **SQLite** – Relational database
- **Uvicorn** – ASGI server
- **Pydantic** – Data validation

---

## 📂 Project Structure

build-blog-api/
│
├── main.py # API routes
├── models.py # Database models
├── schemas.py # Pydantic schemas
├── database.py # DB connection setup
├── requirements.txt
└── README.md


---

## ⚙️ Setup & Run

### 1️⃣ Clone the repository
```bash
git clone <your-github-repo-url>
cd build-blog-api

2️⃣ Create virtual environment
python -m venv venv


Activate:

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the server
uvicorn main:app --reload

5️⃣ Open API docs

👉 http://127.0.0.1:8000/docs

🗄 Database Schema
Author

id (Primary Key)

name (string)

email (string, unique)

Post

id (Primary Key)

title (string)

content (text)

author_id (Foreign Key → Author.id)

Relationship:
One Author can have many Posts.
Deleting an Author will also delete all their Posts (CASCADE).

Author (1) ─────────< (N) Post

📡 API Endpoints
👤 Author Endpoints
Method	Endpoint	Description
POST	/authors	Create a new author
GET	/authors	Retrieve all authors
GET	/authors/{id}	Retrieve author by ID
PUT	/authors/{id}	Update author
DELETE	/authors/{id}	Delete author
GET	/authors/{id}/posts	Get posts by author
📝 Post Endpoints
Method	Endpoint	Description
POST	/posts	Create a new post
GET	/posts	Get all posts (filter by author_id)
GET	/posts/{id}	Get post by ID (with author details)
PUT	/posts/{id}	Update post
DELETE	/posts/{id}	Delete post
🧪 Example Requests
➕ Create Author
POST /authors
{
  "name": "Alice",
  "email": "alice@example.com"
}

➕ Create Post
POST /posts
{
  "title": "My First Post",
  "content": "Hello World!",
  "author_id": 1
}

📄 Get Post with Author
GET /posts/1

{
  "id": 1,
  "title": "My First Post",
  "content": "Hello World!",
  "author": {
    "name": "Alice",
    "email": "alice@example.com"
  }
}

❗ Error Handling

404 Not Found → Resource does not exist

400 Bad Request → Invalid input (e.g., non-existent author_id)

Unique email constraint enforced at DB level

🔍 Query Optimization

JOIN queries are used to fetch posts with author details.

Prevents N+1 query problem by eager loading related data.

📸 Screenshots (Optional)

You may add screenshots of:

Swagger UI (/docs)

Sample API responses

Example:

![Swagger UI](screenshots/swagger.png)

🧪 Testing

You can test the API using:

Swagger UI at /docs

Postman or curl