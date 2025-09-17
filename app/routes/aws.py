from fastapi import APIRouter, HTTPException
from app.db.awsdb import get_bucket_list, get_presigned_url, get_music_hall_pictures_name_list
from app import validators

router = APIRouter(prefix="/storage", tags=["Music Hall Management"])


@router.get("/get-bucket-list/")
def check_aws_connection():
    try:
        return get_bucket_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to AWS S3: {e}")


@router.get("/music-halls/{hall_id}/pictures/{file_name}")
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


@router.get("/music-halls/{hall_id}/pictures")
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
