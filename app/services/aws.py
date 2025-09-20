from app.core.config import settings
from app.db.awsdb import get_s3_resource
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import logging

EXPIRATION_TIME_SECONDS = 180  # 3minutes
BUCKET_NAME = settings.BUCKET_NAME

async def get_bucket_list():
    s3_resource = get_s3_resource()
    try:
        buckets = [bucket.name async for bucket in s3_resource.buckets.all()]
        return {"buckets": buckets}
    except Exception as e:
        raise Exception(f"Failed to retrieve URL: {e}")


async def get_music_hall_pictures_name_list(prefix: str):
    s3_resource = get_s3_resource()
    bucket = await s3_resource.Bucket(BUCKET_NAME)
    try:
        filenames = [
            obj.key.replace(prefix, "").replace(".JPG", "")
            async for obj in bucket.objects.filter(Prefix=prefix)
            if obj.key != prefix
        ]
        return filenames
    except Exception as e:
        raise Exception(f"Failed to retrieve list names: {e}")


async def get_presigned_url(key: str, expiration: int = EXPIRATION_TIME_SECONDS) -> str:
    s3_resource =  get_s3_resource()
    try:
        response = await s3_resource.meta.client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': key},
            ExpiresIn=expiration
        )
        return response
    except (NoCredentialsError, PartialCredentialsError) as e:
        logging.error(f"Credentials error: {e}")
        raise
    except Exception as e:
        logging.error(f"Error generating pre-signed URL: {e}")
        raise
