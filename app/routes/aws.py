from fastapi import APIRouter, HTTPException, Path
from app.services.aws import get_bucket_list, get_presigned_url, get_music_hall_pictures_name_list
from app.core.exceptions import handle_db_exception
from app.core.logger import setup_logger

router = APIRouter(prefix="/storage", tags=["Music Hall Management"])
logger = setup_logger(__name__)


@router.get("/get-bucket-list/")
async def check_aws_connection():
    try:
        return await get_bucket_list()
    except HTTPException:
        raise
    except Exception as e:
        raise handle_db_exception(e)


@router.get("/music-halls/{hall_id}/pictures/{file_name}")
async def get_picture(
        hall_id: int = Path(..., gt=0),
        file_name: str = Path(..., min_length=1)
):
    try:
        key = f"music-halls:{hall_id}:{file_name}.JPG"
        url = await get_presigned_url(key=key)
        if url:
            return {"url": url}
        else:
            raise HTTPException(status_code=404, detail="Picture not found")
    except HTTPException:
        raise
    except Exception as e:
        raise handle_db_exception(e)


@router.get("/music-halls/{hall_id}/pictures")
async def get_picture_filenames(
        hall_id: int = Path(..., gt=0)
):
    try:
        prefix = f"music-halls:{hall_id}:"
        filenames = await get_music_hall_pictures_name_list(prefix=prefix)
        if filenames is None:
            return {"files": []}
        return {"files": filenames}
    except HTTPException:
        raise
    except Exception as e:
        raise handle_db_exception(e)