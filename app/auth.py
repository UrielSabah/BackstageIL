from fastapi import HTTPException, Header
from app.config import SECRET_KEY

def verify_api_key(api_key: str = Header(...)):
    valid_api_key = SECRET_KEY
    if api_key != valid_api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")
