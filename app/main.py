from fastapi import FastAPI, Depends, HTTPException, Header
from app.models import MusicHall, UpdateMusicHall  # Import the Pydantic model
from app.neondb import insert_music_hall, get_music_hall, update_music_hall
from app.config import SECRET_KEY

# Define the FastAPI app
app = FastAPI(
    title="MusicHalls API",
    description="API for technical information for backstage",
    version="1.0.0"
)


def verify_api_key(api_key: str = Header(...)):
    valid_api_key = SECRET_KEY
    if api_key != valid_api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")


@app.get("/", tags=["App"])
def read_root():
    return {"message": "Hello, World!"}


@app.get("/items/{item_id}", tags=["App"])
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


# Retrieve a music hall by ID
@app.get("/music-halls/{hall_id}", response_model=MusicHall, tags=["Music Hall Management"])
async def fetch_music_hall(hall_id: int):
    try:
        # Call the helper function to get the hall
        hall = get_music_hall(hall_id)
        return hall
    except HTTPException as e:
        raise e


# Endpoint to create a new music hall
@app.post("/music-halls/", response_model=MusicHall, tags=["Music Hall Management"])
async def create_music_hall(hall: MusicHall, api_key: str = Depends(verify_api_key)):
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


@app.put("/music-halls/{hall_id}", tags=["Music Hall Management"])
async def update_hall(hall_id: int, hall_data: UpdateMusicHall, api_key: str = Depends(verify_api_key)):
    # Filter out None values from the input
    try:
        updates = hall_data.dict(exclude_unset=True)
        return update_music_hall(hall_id, updates)
    except HTTPException as e:
        raise e
