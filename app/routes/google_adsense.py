from fastapi import APIRouter
import os
from fastapi.responses import FileResponse

router = APIRouter(prefix="/ads", tags=["Users"])


@router.get("/ads.txt", include_in_schema=False, tags=["Music Hall Management"])
async def serve_ads_txt():
    # Path to the ads.txt file in the root directory
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ads.txt"))
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "ads.txt not found"}
