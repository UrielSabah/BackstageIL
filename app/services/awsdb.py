import boto3
from app.core.config import settings
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import logging

EXPIRATION_TIME_SECONDS = 180  # 3minutes
s3_resource = boto3.resource(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.REGION_NAME
)

BUCKET_NAME = settings.BUCKET_NAME

def get_bucket_list():
    try:
        buckets = [bucket.name for bucket in s3_resource.buckets.all()]
        return {"buckets": buckets}
    except Exception as e:
        raise Exception(f"Failed to retrieve URL: {e}")


def get_music_hall_pictures_name_list(prefix: str):
    try:
        filenames = [
            obj.key.replace(prefix, "").replace(".JPG", "")
            for obj in s3_resource.Bucket(BUCKET_NAME).objects.filter(Prefix=prefix) if obj.key != prefix
        ]
        return filenames
    except Exception as e:
        raise Exception(f"Failed to retrieve list names: {e}")


def get_presigned_url(key: str, expiration: int = EXPIRATION_TIME_SECONDS) -> str:
    try:
        response = s3_resource.meta.client.generate_presigned_url(
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
