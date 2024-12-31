import psycopg2
from fastapi import HTTPException
from app.config import DB_URL

# Neon database connection string
DATABASE_URL = DB_URL


# Function to get a database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to database: {e}")


# SQL query to insert data into the music_halls table
INSERT_HALL_SQL = """
INSERT INTO music_halls (
    city, hall_name, email, stage, pipe_height, stage_type
) VALUES (%s, %s, %s, %s, %s, %s)
RETURNING id, city, hall_name;
"""

FETCH_HALL_SQL = """
    SELECT id, city, hall_name, email, stage, pipe_height, stage_type FROM music_halls WHERE id = %s
"""

FETCH_HALL_LIST_SQL = """
    SELECT id, CONCAT(city, ', ', hall_name) AS hall_info FROM music_halls;
"""

DELETE_HALL_SQL = """
   DELETE FROM music_halls WHERE id = %s RETURNING id
"""


# Function to insert data into the music_halls table
def insert_music_hall(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(INSERT_HALL_SQL, data)
        conn.commit()
        inserted_row = cursor.fetchone()  # Fetch the inserted row (id, city, hall_name)
        return inserted_row
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error inserting data: {e}")
    finally:
        cursor.close()
        conn.close()


def get_music_hall(hall_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Query the database
        cursor.execute(FETCH_HALL_SQL, (hall_id,))
        result = cursor.fetchone()

        # If the row does not exist
        if not result:
            raise HTTPException(status_code=404, detail="Music hall not found")

        # Return a dictionary matching the Pydantic model
        return {
            "id": result[0],
            "city": result[1],
            "hall_name": result[2],
            "email": result[3],
            "stage": result[4],
            "pipe_height": result[5],
            "stage_type": result[6]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    finally:
        cursor.close()
        conn.close()


def update_music_hall(hall_id: int, updates: dict):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Prepare the update query dynamically
        set_clause = ", ".join(f"{key} = %s" for key in updates.keys())
        query = f"UPDATE music_halls SET {set_clause} WHERE id = %s RETURNING id"
        values = list(updates.values()) + [hall_id]

        cursor.execute(query, values)
        updated_row = cursor.fetchone()
        conn.commit()

        if not updated_row:
            raise HTTPException(status_code=404, detail="Music hall not found")

        return {"message": "Music hall updated successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    finally:
        cursor.close()
        conn.close()


def get_music_hall_list():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Query the database
        cursor.execute(FETCH_HALL_LIST_SQL)
        results = cursor.fetchall()

        # If no results found
        if not results:
            raise HTTPException(status_code=404, detail="No halls found")

        # Map results to a list of dictionaries
        hall_list = [
            {"id": row[0], "city_and_hall_name": row[1]} for row in results
        ]
        return hall_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    finally:
        cursor.close()
        conn.close()