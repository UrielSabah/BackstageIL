from fastapi import APIRouter, Depends, HTTPException, Path, Body
from app.schemas.neon import MusicHall, UpdateMusicHall  # Import the Pydantic model
from app.services.neon import (insert_music_hall, get_music_hall, update_music_hall, get_music_hall_list,
                               get_music_hall_recommendations)
from app.core.auth import verify_api_key
from app.db.dependencies import get_db_pool
from app.core.exceptions import handle_db_exception
from app.core.logger import setup_logger
import asyncpg

router = APIRouter(prefix="/db", tags=["Music Hall Management"])
logger = setup_logger(__name__)


# Retrieve a music hall list
@router.get("/music-halls-list/")
async def fetch_music_hall_list(db_pool: asyncpg.Pool = Depends(get_db_pool)):
    try:
        hall_list = await get_music_hall_list(db_pool)
        return hall_list
    except HTTPException:
        raise
    except Exception as e:
        raise handle_db_exception(e)

# Retrieve a music hall by ID
@router.get("/music-halls/{hall_id}", response_model=MusicHall)
async def fetch_music_hall(
        hall_id: int = Path(..., gt=0),
        db_pool: asyncpg.Pool = Depends(get_db_pool)
):
    try:
        hall = await get_music_hall(hall_id, db_pool)
        return hall
    except HTTPException:
        raise
    except Exception as e:
        raise handle_db_exception(e)

# Endpoint to create a new music hall
@router.post("/music-halls/")
async def create_music_hall(
        hall: MusicHall,
        api_key: str = Depends(verify_api_key),
        db_pool: asyncpg.Pool = Depends(get_db_pool)
):
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
        inserted_row = await insert_music_hall(hall_data, db_pool)  # Insert the data into the database
        return {
            "id": inserted_row["id"],
            "city": inserted_row["city"],
            "hall_name": inserted_row["hall_name"],
            "email": hall.email,
            "stage": hall.stage,
            "pipe_height": hall.pipe_height,
            "stage_type": hall.stage_type,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise handle_db_exception(e)

@router.put("/music-halls/{hall_id}")
async def update_hall(
        hall_id: int = Path(..., gt=0),
        hall_data: UpdateMusicHall = Body(...),
        api_key: str = Depends(verify_api_key),
        db_pool: asyncpg.Pool = Depends(get_db_pool)
):
    try:
        updates =  hall_data.model_dump(exclude_unset=True)
        return await update_music_hall(hall_id, updates, db_pool)
    except HTTPException:
        raise
    except Exception as e:
        raise handle_db_exception(e)

@router.get("/music-halls/{hall_id}/recommendations")
async def fetch_music_hall_recommendations(
        hall_id: int = Path(..., gt=0),
        db_pool: asyncpg.Pool = Depends(get_db_pool)
):
    try:
        recommendations = await get_music_hall_recommendations(hall_id, db_pool)
        return recommendations
    except HTTPException:
        raise
    except Exception as e:
        raise handle_db_exception(e)

