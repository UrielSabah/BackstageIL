# 🎭 BackstageIL API

A FastAPI-based backend that manages information about music halls, including creation, retrieval, and updating of hall records. Built with Python, PostgreSQL (via Neon), and deployed to Render, with media storage via AWS S3.

## 📚 Documentation

Auto-generated interactive docs:
- [Swagger UI](http://127.0.0.1:8000/docs)
- [ReDoc](http://127.0.0.1:8000/redoc)

---

## 🚀 Features

- **GET**: Retrieve music hall information by ID.
- **POST**: Add new music hall entries.
- **PUT**: Update existing music halls.
- AWS S3 image integration (via `aioboto3`)
- Connected to Neon (PostgreSQL in the cloud)
- Modular FastAPI architecture
- Includes unit tests with Pytest

---

## 🛠️ Tech Stack

- **Python 3.13**
- **FastAPI** (ASGI framework)
- **Uvicorn** (server)
- **PostgreSQL** (via Neon)
- **AWS S3** for image uploads
- **Render** for deployment

---

## ⚙️ Installation

Clone the repository to your local machine:

- git clone https://github.com/UrielSabah/BackstageIL.git

Create a virtual environment and activate it:
```
python -m venv env
source env/bin/activate 
```

Install the required dependencies:
- pip install -r requirements.txt

## Running the API
Start the development server:

```
    uvicorn app.main:app --reload
```
The API will be available at http://127.0.0.1:8000/.

## API Endpoints
#### 1. Retrieve MusicHall(GET)
```
  GET http://127.0.0.1:8000/db/music-halls/<hall_id>
```

| Parameter | Type  | Description                        |
|:----------|:------|:-----------------------------------|
| `hall_id` | `int` | **Required**. Insert hall_id value |

This endpoint retrieves information about a specific hall by its hall_id.

Example Request:
```
  GET http://127.0.0.1:8000/db/music-halls/5
```

Example Response:
```
{
    "city": "Ashdod",
    "hall_name": "Mamila 1",
    "email": "mamila@example.com",
    "stage": true,
    "pipe_height": 14,
    "stage_type": "raised"
}
```
###

#### 2. Add a new Music Hall (POST) 
```
  POST http://127.0.0.1:8000/db/music-halls/
```

This endpoint allows you to add a new hall 

Example Request:
```
```
Body: 
```
```

Example Response (for new Hall):
```
```


#### 3. Update an existing Music Hall (PUT) 
```
  PUT http://127.0.0.1:8000/db/music-halls/<hall_id>
```

This endpoint allows you to update an existing hall 

Example Request:
```
```
Body: 
```
```
Example Response (for updated Hall):
```
```


## Run Tests
You can run the tests by executing the test_app.py file:
```
 PYTHONPATH=. pytest tests/test_main.py -v
```




