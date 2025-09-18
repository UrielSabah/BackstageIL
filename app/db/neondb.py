from fastapi import HTTPException
from app.config import DB_URL
import asyncpg


DATABASE_URL = DB_URL


# SQL query to insert data into the music_halls table
INSERT_HALL_SQL = """
INSERT INTO music_halls (
    city, hall_name, email, stage, pipe_height, stage_type
) VALUES ($1, $2, $3, $4, $5, $6)
RETURNING id, city, hall_name;
"""

FETCH_HALL_SQL = """
    SELECT id, city, hall_name, email, stage, pipe_height, stage_type FROM music_halls WHERE id = $1
"""

DELETE_HALL_SQL = """
   DELETE FROM music_halls WHERE id = $1 RETURNING id
"""

FETCH_HALL_RECOMMENDATIONS_SQL = """
    SELECT recommendation, update_date FROM music_hall_recommendations WHERE hall_id = $1 order by update_date desc
"""

FETCH_HALL_LIST_SQL = """
    SELECT id, CONCAT(city, ', ', hall_name) AS hall_info FROM music_halls;
"""


async def get_music_hall_list():
    conn = await asyncpg.connect(DB_URL)
    try:
        results = await conn.fetch(FETCH_HALL_LIST_SQL)
        if not results:
            raise HTTPException(status_code=404, detail="No halls found")

        hall_list = [
            {"id": row[0], "city_and_hall_name": row[1]} for row in results
        ]
        return hall_list

    finally:
        await conn.close()


async def get_music_hall(hall_id: int):
    conn = await asyncpg.connect(DB_URL)
    try:
        result = await conn.fetchrow(FETCH_HALL_SQL, hall_id)
        if not result:
            raise HTTPException(status_code=404, detail="Music hall not found")
        return dict(result)
    finally:
        await conn.close()


async def insert_music_hall(data: tuple):
    conn = await asyncpg.connect(DB_URL)
    try:
        inserted_row = await conn.fetchrow(INSERT_HALL_SQL, *data)
        return dict(inserted_row)
    finally:
        await conn.close()


async def update_music_hall(hall_id: int, updates: dict) -> dict:
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    # Build dynamic query using $1, $2, ... placeholders
    set_clause = ", ".join(f"{key} = ${i+1}" for i, key in enumerate(updates.keys()))
    values = list(updates.values()) + [hall_id]  # hall_id is last placeholder

    query = f"""
        UPDATE music_halls
        SET {set_clause}
        WHERE id = ${len(values)}
        RETURNING id, city, hall_name, email, stage, pipe_height, stage_type;
    """

    conn = await asyncpg.connect(DB_URL)
    try:
        updated_row = await conn.fetchrow(query, *values)
        if not updated_row:
            raise HTTPException(status_code=404, detail="Music hall not found")
        return dict(updated_row)
    finally:
        await conn.close()


async def get_music_hall_recommendations(hall_id: int):
    conn = await asyncpg.connect(DB_URL)
    try:
        results = await conn.fetch(FETCH_HALL_RECOMMENDATIONS_SQL, hall_id)
        if not results:
            return []

        hall_list_recommendations = [
             {"update_date": row[1].date(), "recommendation": row[0], } for row in results
        ]
        return hall_list_recommendations
    finally:
        await conn.close()

