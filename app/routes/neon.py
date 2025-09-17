from fastapi import APIRouter, Depends, HTTPException
from app import validators
from app.schemas.models import MusicHall, UpdateMusicHall  # Import the Pydantic model
from app.db.neondb import (insert_music_hall, get_music_hall, update_music_hall, get_music_hall_list,
                           get_music_hall_recommendations)
from app.auth import verify_api_key


router = APIRouter(prefix="/db", tags=["Music Hall Management"])


# Retrieve a music hall list
@router.get("/music-halls-list/", tags=["Music Hall Management"])
async def fetch_music_hall_list():
    try:
        # Call the helper function to get the hall
        hall_list = get_music_hall_list()
        return hall_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Retrieve a music hall by ID
@router.get("/music-halls/{hall_id}", response_model=MusicHall, tags=["Music Hall Management"])
async def fetch_music_hall(hall_id: int):
    try:
        if not validators.validate_all_inputs_as_integers(hall_id):
            raise HTTPException(status_code=422, detail=validators.RAISE_422)
        # Call the helper function to get the hall
        hall = get_music_hall(hall_id)
        return hall
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to create a new music hall
@router.post("/music-halls/", response_model=MusicHall, tags=["Music Hall Management"])
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/music-halls/{hall_id}", tags=["Music Hall Management"])
async def update_hall(hall_id: int, hall_data: UpdateMusicHall, api_key: str = Depends(verify_api_key)):
    # Filter out None values from the input
    try:
        if not validators.validate_all_inputs_as_integers(hall_id):
            raise HTTPException(status_code=422, detail=validators.RAISE_422)
        updates = hall_data.model_dump(exclude_unset=True)
        return update_music_hall(hall_id, updates)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Retrieve all Recommendations of a music hall by ID
@router.get("/music-halls/{hall_id}/recommendations", tags=["Music Hall Management"])
async def fetch_music_hall_recommendations(hall_id: int):
    try:
        if not validators.validate_all_inputs_as_integers(hall_id):
            raise HTTPException(status_code=422, detail=validators.RAISE_422)
        # Call the helper function to get the hall
        recommendations = get_music_hall_recommendations(hall_id)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
