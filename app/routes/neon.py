from fastapi import APIRouter, Depends, Path, Body, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.neon import (
    MusicHall,
    UpdateMusicHall,
    MusicHallResponse,
    MusicHallListItem,
    MusicHallRecommendation,
)
from app.services.neon import (
    insert_music_hall,
    get_music_hall,
    update_music_hall,
    get_music_hall_list,
    get_music_hall_recommendations,
    delete_music_hall,
)
from app.core.auth import verify_api_key
from app.db.dependencies import get_async_session

router = APIRouter(prefix="/db", tags=["Music Hall Management"])


@router.get(
    "/music-halls",
    response_model=list[MusicHallListItem],
    summary="List all music halls",
    description="Retrieve a list of all music halls with their IDs and combined city/hall name",
)
async def fetch_music_hall_list(session: AsyncSession = Depends(get_async_session)):
    hall_list = await get_music_hall_list(session)
    return hall_list


@router.get(
    "/music-halls/{hall_id}",
    response_model=MusicHallResponse,
    summary="Get music hall by ID",
    description="Retrieve detailed information about a specific music hall by its ID",
)
async def fetch_music_hall(
    hall_id: int = Path(..., gt=0, description="Unique identifier of the music hall"),
    session: AsyncSession = Depends(get_async_session),
):
    hall = await get_music_hall(hall_id, session)
    return hall


@router.post(
    "/music-halls",
    response_model=MusicHallResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new music hall",
    description="Create a new music hall entry. Requires API key authentication.",
)
async def create_music_hall(
    hall: MusicHall,
    api_key: str = Depends(verify_api_key),
    session: AsyncSession = Depends(get_async_session),
):
    inserted = await insert_music_hall(session, hall)
    return inserted


@router.put(
    "/music-halls/{hall_id}",
    response_model=MusicHallResponse,
    summary="Update a music hall",
    description="Update an existing music hall. Only provided fields will be updated. Requires API key authentication.",
)
async def update_hall(
    hall_id: int = Path(..., gt=0, description="Unique identifier of the music hall to update"),
    hall_data: UpdateMusicHall = Body(...),
    api_key: str = Depends(verify_api_key),
    session: AsyncSession = Depends(get_async_session),
):
    updates = hall_data.model_dump(exclude_unset=True)
    return await update_music_hall(hall_id, updates, session)


@router.delete(
    "/music-halls/{hall_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a music hall",
    description="Delete a music hall by ID. Requires API key authentication.",
)
async def delete_hall(
    hall_id: int = Path(..., gt=0, description="Unique identifier of the music hall to delete"),
    api_key: str = Depends(verify_api_key),
    session: AsyncSession = Depends(get_async_session),
):
    await delete_music_hall(hall_id, session)


@router.get(
    "/music-halls/{hall_id}/recommendations",
    response_model=list[MusicHallRecommendation],
    summary="Get music hall recommendations",
    description="Retrieve all recommendations for a specific music hall, ordered by most recent first",
)
async def fetch_music_hall_recommendations(
    hall_id: int = Path(..., gt=0, description="Unique identifier of the music hall"),
    session: AsyncSession = Depends(get_async_session),
):
    recommendations = await get_music_hall_recommendations(hall_id, session)
    return recommendations
