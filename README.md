# HNG13-oneExcellent — here’s a **comprehensive `README.md`** for your FastAPI + async SQLAlchemy project that analyzes and stores string properties in PostgreSQL.

This guide includes:
✅ full project overview
✅ code and process explanation
✅ local installation (no Docker)
✅ example API calls and responses (success & failure)
✅ `requirements.txt` section

---

## 🧾 README.md

````markdown
# 🧠 String Analysis REST API

This project is a **FastAPI-based asynchronous REST API** that analyzes text strings and stores their computed properties in a **PostgreSQL** database.

It demonstrates:
- Asynchronous I/O with **FastAPI + SQLAlchemy (async)**
- **PostgreSQL JSONB** storage
- **Rule-based natural language filtering**
- Clean RESTful design with proper HTTP status codes

---

## 📘 Features

For each analyzed string, the API computes and stores:

| Property | Description |
|-----------|-------------|
| `length` | Number of characters |
| `is_palindrome` | Whether the string reads the same backward and forward (case-insensitive) |
| `unique_characters` | Count of distinct characters |
| `word_count` | Number of words (split by whitespace) |
| `sha256_hash` | Unique SHA-256 hash identifier |
| `character_frequency_map` | Mapping of each character to its count |

---

## 🧩 Endpoints Overview

| Method | Endpoint | Description |
|---------|-----------|-------------|
| `POST` | `/strings` | Analyze and store a new string |
| `GET` | `/strings/{string_value}` | Retrieve stored string data |
| `GET` | `/strings` | List all strings with optional filters |
| `GET` | `/strings/filter-by-natural-language` | Filter using plain English queries |
| `DELETE` | `/strings/{string_value}` | Delete a string from the system |

---

## 🏗️ How It Works

1. **User sends a string** to `/strings` via `POST`.
2. The API computes all properties:
   - Detects palindromes (case-insensitive)
   - Counts unique characters and words
   - Computes SHA-256 hash
   - Builds a character frequency map
3. The record is stored in PostgreSQL (`analyzed_strings` table).
4. You can query or filter strings later by computed attributes or even natural language.

---

## 🧠 Code Description (main.py)

| Section | Summary |
|----------|----------|
| **Model** | `AnalyzedString` defines columns: `id (sha256)`, `value`, `properties (JSONB)`, `created_at`. |
| **Schema** | Pydantic models for request/response validation. |
| **Utility Functions** | - `analyze_string()` computes properties.<br>- `parse_nl_query()` interprets English phrases like "all single word palindromic strings". |
| **Routes** | Implements all RESTful endpoints with error handling and filtering. |
| **Database Setup** | Uses `create_async_engine` with `asyncpg`. Table auto-creates at startup. |

---

## ⚙️ Installation (Local, No Docker)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/string-analysis-api.git
cd string-analysis-api
````

### 2️⃣ Create and activate a virtual environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set up PostgreSQL

Ensure PostgreSQL is installed and running locally.

Create a database:

```bash
psql -U postgres
CREATE DATABASE stringdb;
```

Update `DATABASE_URL` in `main.py` (if needed):

```python
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/stringdb"
```

### 5️⃣ Run the server

```bash
uvicorn main:app --reload
```

Server runs at:

```
http://127.0.0.1:8000
```

---

## 📦 requirements.txt

```txt
fastapi==0.115.0
uvicorn[standard]==0.30.0
SQLAlchemy==2.0.36
asyncpg==0.29.0
pydantic==2.8.2
```

*(versions may update — these are known working ones)*

---

## 🔍 Example API Usage

### ➕ Create / Analyze String

**Request**

```bash
curl -X POST "http://127.0.0.1:8000/strings" \
     -H "Content-Type: application/json" \
     -d '{"value": "racecar"}'
```

**Response (201 Created)**

```json
{
  "id": "d4c4f0e3a6f7f8bbf705a7d5edb964a1e3fa24e196ceef232b6f21c7f57a2a74",
  "value": "racecar",
  "properties": {
    "length": 7,
    "is_palindrome": true,
    "unique_characters": 5,
    "word_count": 1,
    "sha256_hash": "d4c4f0e3a6f7f8bbf705a7d5edb964a1e3fa24e196ceef232b6f21c7f57a2a74",
    "character_frequency_map": {
      "r": 2,
      "a": 2,
      "c": 2,
      "e": 1
    }
  },
  "created_at": "2025-10-22T10:00:00Z"
}
```

---

### 🔍 Get a Specific String

**Request**

```bash
curl "http://127.0.0.1:8000/strings/racecar"
```

**Response (200 OK)**

```json
{
  "id": "d4c4f0e3a6f7f8bbf705a7d5edb964a1e3fa24e196ceef232b6f21c7f57a2a74",
  "value": "racecar",
  "properties": {
    "length": 7,
    "is_palindrome": true,
    "unique_characters": 5,
    "word_count": 1,
    "sha256_hash": "d4c4f0e3a6f7f8bbf705a7d5edb964a1e3fa24e196ceef232b6f21c7f57a2a74",
    "character_frequency_map": {
      "r": 2,
      "a": 2,
      "c": 2,
      "e": 1
    }
  },
  "created_at": "2025-10-22T10:00:00Z"
}
```

---

## ❌ Example Failure Case

### Attempt to Create a Duplicate String

**Request**

```bash
curl -X POST "http://127.0.0.1:8000/strings" \
     -H "Content-Type: application/json" \
     -d '{"value": "racecar"}'
```

**Response (409 Conflict)**

```json
{
  "detail": "String already exists in the system"
}
```

---

## 🌐 Filtering Examples

**Query by Filters**

```bash
curl "http://127.0.0.1:8000/strings?is_palindrome=true&min_length=5"
```

**Query by Natural Language**

```bash
curl "http://127.0.0.1:8000/strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings"
```

---


## 🧰 Project Structure

```
HNG13-one/
│
├── app.py              # Main FastAPI application
├── requirements.txt     # Dependencies
├── README.md            # This file
└── venv/                # Local virtual environment (ignored in git)
```

---

## 🧑‍💻 Author

Developed by **Binael Nchekwube**
© 2025 — Open to contributions.


