import boto3
from app.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME, BUCKET_NAME

s3_resource = boto3.resource(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME
)


def get_bucket_list():
    try:
        buckets = [bucket.name for bucket in s3_resource.buckets.all()]
        return {"buckets": buckets}
    except Exception as e:
        raise Exception(f"Failed to retrieve URL: {e}")
