import logging
from app.core.config import settings
from app.db.awsdb import get_s3_resource, get_s3_client

logger = logging.getLogger(__name__)

BUCKET_NAME = settings.BUCKET_NAME
EXPIRATION_TIME_SECONDS = 180  # 3 minutes


async def get_bucket_list():
    s3 = get_s3_resource()
    try:
        buckets = [bucket.name async for bucket in s3.buckets.all()]
        return {"buckets": buckets}
    except Exception as e:
        logger.error(f"Failed to list buckets: {e}")
        raise


async def get_music_hall_pictures_name_list(prefix: str):
    s3 = get_s3_resource()
    bucket = await s3.Bucket(BUCKET_NAME)
    try:
        filenames = [
            obj.key.replace(prefix, "").removesuffix(".JPG")
            async for obj in bucket.objects.filter(Prefix=prefix)
            if obj.key != prefix
        ]
        return filenames
    except Exception as e:
        logger.error(f"Failed to retrieve object list: {e}")
        raise


async def get_presigned_url(key: str,expiration: int = EXPIRATION_TIME_SECONDS ) -> str:
    s3 = get_s3_client()
    try:
        response = await s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET_NAME, "Key": key},
        ExpiresIn=expiration
        )
        return response
    except Exception as e:
        logger.error(f"Failed to retrieve object list: {e}")
        raise
