import aioboto3
from app.core.config import settings
import logging
from typing import Optional, Any
from functools import lru_cache

EXPIRATION_TIME_SECONDS = 180
BUCKET_NAME = settings.BUCKET_NAME

_session: Optional[aioboto3.Session] = None
_s3_resource_cm: Optional[Any] = None
_s3_client_cm: Optional[Any] = None
_s3_resource: Optional[Any] = None
_s3_client: Optional[Any] = None


async def init_aws():
    """Initialize S3 resource and client."""
    global _session, _s3_resource_cm, _s3_client_cm, _s3_resource, _s3_client

    if _session is None:
        _session = aioboto3.Session()

    if _s3_resource is None:
        _s3_resource_cm = _session.resource(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME,
        )
        _s3_resource = await _s3_resource_cm.__aenter__()

    if _s3_client is None:
        _s3_client_cm = _session.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME,
        )
        _s3_client = await _s3_client_cm.__aenter__()

    logging.info("AWS S3 resource and client initialized.")

async def close_aws():
    """Close S3 resource and client."""
    global _s3_resource_cm, _s3_client_cm, _s3_resource, _s3_client

    if _s3_resource_cm:
        await _s3_resource_cm.__aexit__(None, None, None)
        _s3_resource_cm = None
        _s3_resource = None

    if _s3_client_cm:
        await _s3_client_cm.__aexit__(None, None, None)
        _s3_client_cm = None
        _s3_client = None

    logging.info("AWS S3 resource and client closed.")

@lru_cache(maxsize=1)
def get_s3_resource():
    global _s3_resource
    return _s3_resource

@lru_cache(maxsize=1)
def get_s3_client():
    global _s3_client
    return _s3_client
