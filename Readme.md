# 🎭 BackstageIL API

FastAPI backend for music hall information: CRUD, list, and recommendations. Uses **PostgreSQL (Neon)** and **Render** for deployment.

## 📚 Docs

- **Swagger UI:** http://127.0.0.1:8000/docs  
- **ReDoc:** http://127.0.0.1:8000/redoc  

---

## 🚀 Features

- **Music halls:** list, get by ID, create, update, delete
- **Recommendations:** get recommendations per hall
- **Auth:** API key (e.g. `X-API-Key` header) for create/update/delete
- **Health:** `GET /health/`

---

## 🛠️ Stack

- Python 3.13
- FastAPI, Uvicorn
- SQLAlchemy 2 (async) + asyncpg
- PostgreSQL (Neon)
- Render (Docker)

---

## ⚙️ Setup

**Clone and venv:**

```bash
git clone https://github.com/UrielSabah/BackstageIL.git
cd BackstageIL
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**Environment:** create a `.env` in the project root with:

- `DB_URL` – PostgreSQL URL (e.g. Neon; use `?sslmode=require` if required)
- `SECRET_KEY` – API key for protected endpoints

---

## 🏃 Run

From the project root:

```bash
export PYTHONPATH=.
uvicorn app.main:app --reload
```

API: http://127.0.0.1:8000  

---

## 🐳 Docker

**Local (uses `.env`, e.g. Neon):**

```bash
docker compose up --build
```

API: http://localhost:10000  

**Production:** use the `Dockerfile` on Render (or any Docker host). Set `DB_URL` and `SECRET_KEY` in the environment.

---

## 📡 API overview

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/health/` | No | Health check |
| GET | `/db/music-halls` | No | List halls (id, city_and_hall_name) |
| GET | `/db/music-halls/{id}` | No | Get hall by ID |
| POST | `/db/music-halls` | API key | Create hall |
| PUT | `/db/music-halls/{id}` | API key | Update hall |
| DELETE | `/db/music-halls/{id}` | API key | Delete hall |
| GET | `/db/music-halls/{id}/recommendations` | No | List recommendations for hall |

**Create/update body (POST/PUT):** `city`, `hall_name`, `email`, `stage`, `pipe_height`, `stage_type` (optional on PUT).  
**Auth:** send API key in header, e.g. `X-API-Key: <SECRET_KEY>`.

---

## 🧪 Tests

```bash
PYTHONPATH=. pytest tests/ -v
```

---

## 📁 Layout

- `app/` – application code  
  - `core/` – config, auth, exceptions, logger  
  - `db/` – Neon connection, session, SQLAlchemy models  
  - `routes/` – HTTP endpoints  
  - `schemas/` – Pydantic request/response models  
  - `services/` – business logic  
- `static/` – static files (e.g. `ads.txt`)  
- `tests/` – pytest tests  

