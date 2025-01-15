from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware

from app import validators
from app.models import MusicHall, UpdateMusicHall  # Import the Pydantic model
from app.neondb import insert_music_hall, get_music_hall, update_music_hall, get_music_hall_list, get_music_hall_recommendations
from fastapi.responses import FileResponse
from app.awsdb import get_bucket_list, get_presigned_url, get_music_hall_pictures_name_list
import os
from app.config import SECRET_KEY


# Define the FastAPI app
app = FastAPI(
    title="BackstageIL API",
    description="API for technical information for backstage's",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, replace '*' with specific URLs if needed
    allow_credentials=True,
    allow_methods=["GET"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


def verify_api_key(api_key: str = Header(...)):
    valid_api_key = SECRET_KEY
    if api_key != valid_api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")


@app.get("/", tags=["Music Hall Management"])
def read_root():
    return {"message": "ITS ALIVE!!!"}


@app.get("/ads.txt", include_in_schema=False, tags=["Music Hall Management"])
async def serve_ads_txt():
    # Path to the ads.txt file in the root directory
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ads.txt"))
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "ads.txt not found"}


'''
----->AWS<-----
'''


@app.get("/get-bucket-list/" , tags=["Music Hall Management"])
def check_aws_connection():
    try:
        return get_bucket_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to AWS S3: {e}")


@app.get("/music-halls/{hall_id}/pictures/{file_name}" , tags=["Music Hall Management"])
async def get_picture(hall_id: int, file_name: str):
    try:
        if not validators.validate_all_inputs_as_integers(hall_id, file_name):
            raise HTTPException(status_code=422, detail=validators.RAISE_422)
        key = f"music-halls:{hall_id}:{file_name}.JPG"
        url = get_presigned_url(key=key)
        if url:
            return {"url": url}
        else:
            raise HTTPException(status_code=404, detail="Picture not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/music-halls/{hall_id}/pictures" , tags=["Music Hall Management"])
async def get_picture_filenames(hall_id: int):
    try:
        if not validators.validate_all_inputs_as_integers(hall_id):
            raise HTTPException(status_code=422, detail=validators.RAISE_422)
        prefix = f"music-halls:{hall_id}:"
        filenames = get_music_hall_pictures_name_list(prefix=prefix)
        if filenames is None:
            return {"files": []}
        return {"files": filenames}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

'''
----->AWS<-----
'''

'''
----->SQL - NEON<-----
'''


# Retrieve a music hall list
@app.get("/music-halls-list/", tags=["Music Hall Management"])
async def fetch_music_hall_list():
    try:
        # Call the helper function to get the hall
        hall_list = get_music_hall_list()
        return hall_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Retrieve a music hall by ID
@app.get("/music-halls/{hall_id}", response_model=MusicHall, tags=["Music Hall Management"])
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/music-halls/{hall_id}", tags=["Music Hall Management"])
async def update_hall(hall_id: int, hall_data: UpdateMusicHall, api_key: str = Depends(verify_api_key)):
    # Filter out None values from the input
    try:
        if not validators.validate_all_inputs_as_integers(hall_id):
            raise HTTPException(status_code=422, detail=validators.RAISE_422)
        updates = hall_data.dict(exclude_unset=True)
        return update_music_hall(hall_id, updates)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Retrieve all Recommendations of a music hall by ID
@app.get("/music-halls/{hall_id}/recommendations", tags=["Music Hall Management"])
async def fetch_music_hall(hall_id: int):
    try:
        if not validators.validate_all_inputs_as_integers(hall_id):
            raise HTTPException(status_code=422, detail=validators.RAISE_422)
        # Call the helper function to get the hall
        recommendations = get_music_hall_recommendations(hall_id)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
