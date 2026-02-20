from fastapi import HTTPException, Header

from app.core.config import settings


def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key", description="API key for create/update/delete")) -> str:
    """Validate API key from X-API-Key header. Raises 403 if invalid."""
    if x_api_key != settings.SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key
