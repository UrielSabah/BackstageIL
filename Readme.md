# Readme
Auto-generated docs at:
```
   Swagger UI: http://127.0.0.1:8000/docs
   ReDoc: http://127.0.0.1:8000/redoc
```

#### The CSV created is the original input, the dataframe calculation is printed on the terminal when run the main.py file

The API allows you to retrieve flight information, add new flights, and update existing flight information.

## Features

- **GET**: Retrieve hall information by hall_id.
- **POST**: Add a new hall.

## Prerequisites
Make sure you have the following installed:
- I used: Python 3.13

## Installation
Install FastAPI and an ASGI server (e.g., Uvicorn):
```
    pip install fastapi uvicorn
```
Clone the repository to your local machine:

- git clone https://github.com/UrielSabah/BackstageIL.git

Install the required dependencies:
- pip3 install -r requirements.txt

## Running the API
Start the FastAPI server locally:
```
    uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:8000/.

## API Endpoints
#### 1. Retrieve MusicHall(GET)
```
  GET http://127.0.0.1:8000/music-halls/<hall_id>
```

| Parameter | Type  | Description                        |
|:----------|:------|:-----------------------------------|
| `hall_id` | `int` | **Required**. Insert hall_id value |

This endpoint retrieves information about a specific hall by its hall_id.

Example Request:
```
  GET http://127.0.0.1:8000/music-halls/5
```

Example Response:
```

```
###

#### 2. Add or Update Flight (POST) 
```
  POST http://127.0.0.1:8000/music-halls/
```

This endpoint allows you to add a new hall 

Example Request:
```
```
Body: 
```
```

Example Response (for new flight):
```
```

Example Response (for updated flight):
```
```


## Run Tests
You can run the tests by executing the test_app.py file:
- python -m unittest test_main.py



