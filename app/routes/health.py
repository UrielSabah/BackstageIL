from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Music Hall Management"])

@router.get("/")
def read_root():
    return {"message": "ITS ALIVE!!!"}