import aioboto3
from app.core.config import settings
import logging
from typing import Optional

logger = logging.getLogger(__name__)

_session: Optional[aioboto3.Session] = None
_s3_resource = None
_s3_client = None

BUCKET_NAME = settings.BUCKET_NAME
EXPIRATION_TIME_SECONDS = 180  # 3 minutes


async def init_aws() -> None:
    """Initialize aioboto3 session, S3 resource, and client (async)."""
    global _session, _s3_resource, _s3_client

    if _session is None:
        _session = aioboto3.Session()

    if _s3_resource is None:
        # Create resource via async context manager
        resource_cm = _session.resource(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME,
        )
        _s3_resource = await resource_cm.__aenter__()

    if _s3_client is None:
        client_cm = _session.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME,
        )
        _s3_client = await client_cm.__aenter__()

    logger.info("AWS S3 resource and client initialized.")


async def close_aws() -> None:
    """Gracefully close the S3 resource and client."""
    global _s3_resource, _s3_client

    if _s3_resource:
        try:
            await _s3_resource.close()
        except Exception as e:
            logger.warning(f"Error closing S3 resource: {e}")
        finally:
            _s3_resource = None

    if _s3_client:
        try:
            await _s3_client.close()
        except Exception as e:
            logger.warning(f"Error closing S3 client: {e}")
        finally:
            _s3_client = None

    logger.info("AWS S3 resource and client closed.")


def get_s3_resource():
    if _s3_resource is None:
        raise RuntimeError("S3 resource not initialized. Call init_aws() first.")
    return _s3_resource


def get_s3_client():
    if _s3_client is None:
        raise RuntimeError("S3 client not initialized. Call init_aws() first.")
    return _s3_client
