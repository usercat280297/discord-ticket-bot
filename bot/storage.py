import os
import logging
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from typing import Optional

logger = logging.getLogger(__name__)


def _get_s3_client():
    return boto3.client(
        's3',
        region_name=os.getenv('AWS_REGION'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )


def generate_presigned_get_url(bucket: str, key: str, expires_in: int = 3600) -> Optional[str]:
    """Generate a presigned GET URL for an existing object.

    Returns the URL string or None on error.
    """
    client = _get_s3_client()
    try:
        url = client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=expires_in
        )
        return url
    except (BotoCoreError, ClientError) as e:
        logger.exception("Failed to generate presigned GET URL: %s", e)
        return None


def generate_presigned_put_url(bucket: str, key: str, expires_in: int = 3600, content_type: Optional[str] = None) -> Optional[str]:
    """Generate a presigned PUT URL for uploading an object directly from a client.

    Use `content_type` to restrict the Content-Type of the upload.
    """
    client = _get_s3_client()
    params = {'Bucket': bucket, 'Key': key}
    if content_type:
        params['ContentType'] = content_type

    try:
        url = client.generate_presigned_url(
            'put_object',
            Params=params,
            ExpiresIn=expires_in
        )
        return url
    except (BotoCoreError, ClientError) as e:
        logger.exception("Failed to generate presigned PUT URL: %s", e)
        return None


def upload_fileobj(fileobj, bucket: str, key: str, extra_args: Optional[dict] = None) -> bool:
    """Upload a file-like object to S3. Returns True on success."""
    client = _get_s3_client()
    try:
        client.upload_fileobj(fileobj, bucket, key, ExtraArgs=extra_args or {})
        return True
    except (BotoCoreError, ClientError) as e:
        logger.exception("S3 upload_fileobj failed: %s", e)
        return False
