from fastapi import HTTPException, Header
from app.core.config import settings

def verify_api_key(api_key: str = Header(...)):
    valid_api_key = settings.SECRET_KEY
    if api_key != valid_api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")
