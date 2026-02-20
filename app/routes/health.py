from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", summary="Health check")
async def health_check():
    """Simple liveness check; no DB dependency."""
    return {"message": "ITS ALIVE!!!"}