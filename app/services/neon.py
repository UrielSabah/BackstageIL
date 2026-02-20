"""
Music hall domain services using SQLAlchemy async session (Neon PostgreSQL).
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    MusicHallNotFoundError,
    MusicHallListEmptyError,
    NoFieldsToUpdateError,
    InvalidUpdateFieldsError,
)
from app.db.models import MusicHallModel, MusicHallRecommendationModel
from app.schemas.neon import MusicHall

# Allowed columns for updates (whitelist to prevent SQL injection)
ALLOWED_UPDATE_COLUMNS = {
    "city", "hall_name", "email", "stage", "pipe_height", "stage_type"
}


async def get_music_hall_list(session: AsyncSession) -> list[dict]:
    """
    Retrieve a list of all music halls (id and city_and_hall_name).

    Raises:
        MusicHallListEmptyError: If no music halls are found in the database.
    """
    result = await session.execute(
        select(MusicHallModel.id, MusicHallModel.city, MusicHallModel.hall_name)
    )
    rows = result.all()
    if not rows:
        raise MusicHallListEmptyError()
    return [
        {
            "id": r.id,
            "city_and_hall_name": f"{r.city}, {r.hall_name}",
        }
        for r in rows
    ]


async def get_music_hall(hall_id: int, session: AsyncSession) -> dict:
    """
    Retrieve a music hall by its ID.

    Raises:
        MusicHallNotFoundError: If the music hall with the given ID does not exist.
    """
    result = await session.execute(
        select(MusicHallModel).where(MusicHallModel.id == hall_id)
    )
    hall = result.scalar_one_or_none()
    if hall is None:
        raise MusicHallNotFoundError(hall_id)
    return hall.to_dict()


async def insert_music_hall(session: AsyncSession, hall: MusicHall) -> dict:
    """
    Insert a new music hall.

    Args:
        session: Async SQLAlchemy session.
        hall: Pydantic MusicHall model (request body).

    Returns:
        Inserted row as dict with id, city, hall_name, email, stage, pipe_height, stage_type.
    """
    stage_type_val = hall.stage_type.value if hasattr(hall.stage_type, "value") else hall.stage_type
    model = MusicHallModel(
        city=hall.city,
        hall_name=hall.hall_name,
        email=hall.email,
        stage=hall.stage,
        pipe_height=hall.pipe_height,
        stage_type=stage_type_val,
    )
    session.add(model)
    await session.flush()
    return model.to_dict()


async def update_music_hall(
    hall_id: int,
    updates: dict[str, object],
    session: AsyncSession,
) -> dict:
    """
    Update an existing music hall.

    Raises:
        NoFieldsToUpdateError: If updates is empty.
        InvalidUpdateFieldsError: If any key is not in ALLOWED_UPDATE_COLUMNS.
        MusicHallNotFoundError: If the music hall does not exist.
    """
    if not updates:
        raise NoFieldsToUpdateError()

    invalid_columns = set(updates.keys()) - ALLOWED_UPDATE_COLUMNS
    if invalid_columns:
        raise InvalidUpdateFieldsError(invalid_columns)

    result = await session.execute(
        select(MusicHallModel).where(MusicHallModel.id == hall_id)
    )
    hall = result.scalar_one_or_none()
    if hall is None:
        raise MusicHallNotFoundError(hall_id)

    for key, value in updates.items():
        if hasattr(value, "value"):  # enum
            setattr(hall, key, value.value)
        else:
            setattr(hall, key, value)
    await session.flush()
    return hall.to_dict()


async def get_music_hall_recommendations(
    hall_id: int,
    session: AsyncSession,
) -> list[dict]:
    """
    Retrieve recommendations for a music hall, newest first.
    """
    result = await session.execute(
        select(MusicHallRecommendationModel)
        .where(MusicHallRecommendationModel.hall_id == hall_id)
        .order_by(MusicHallRecommendationModel.update_date.desc())
    )
    recommendations = result.scalars().all()
    return [r.to_dict() for r in recommendations]


async def delete_music_hall(hall_id: int, session: AsyncSession) -> None:
    """
    Delete a music hall by ID.

    Raises:
        MusicHallNotFoundError: If the music hall does not exist.
    """
    result = await session.execute(
        select(MusicHallModel).where(MusicHallModel.id == hall_id)
    )
    hall = result.scalar_one_or_none()
    if hall is None:
        raise MusicHallNotFoundError(hall_id)
    await session.delete(hall)
    await session.flush()
