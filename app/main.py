from fastapi import FastAPI, HTTPException
from app.models import MusicHall, UpdateMusicHall  # Import the Pydantic model
from app.neondb import insert_music_hall, get_music_hall, update_music_hall

# Define the FastAPI app
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


# Endpoint to create a new music hall
@app.post("/music-halls/", response_model=MusicHall)
async def create_music_hall(hall: MusicHall):
    # Prepare data tuple for database insertion
    hall_data = (
        hall.city,
        hall.hall_name,
        hall.email,
        hall.stage,
        hall.pipe_height,
        hall.stage_type
    )

    try:
        inserted_row = insert_music_hall(hall_data)  # Insert the data into the database
        return {
            "id": inserted_row[0],
            "city": inserted_row[1],
            "hall_name": inserted_row[2],
            "email": hall.email,
            "stage": hall.stage,
            "pipe_height": hall.pipe_height,
            "stage_type": hall.stage_type,
        }
    except HTTPException as e:
        raise e


# Retrieve a music hall by ID
@app.get("/music-halls/{hall_id}", response_model=MusicHall)
async def fetch_music_hall(hall_id: int):
    try:
        # Call the helper function to get the hall
        hall = get_music_hall(hall_id)
        return hall
    except HTTPException as e:
        raise e


@app.put("/music-halls/{hall_id}")
async def update_hall(hall_id: int, hall_data: UpdateMusicHall):
    # Filter out None values from the input
    updates = hall_data.dict(exclude_unset=True)
    return update_music_hall(hall_id, updates)
