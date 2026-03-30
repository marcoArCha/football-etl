import json
import boto3
from loguru import logger
from datetime import datetime
from config.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    S3_BUCKET_NAME,
)


def get_s3_client():
    """
    Creates and returns a boto3 S3 client.
    Credentials are loaded from environment variables.
    """
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )


def build_s3_key() -> str:
    """
    Builds the S3 file path with timestamp partitioning.

    Returns:
        S3 key string e.g. 'players/2024/03/29/players_20240329_153000.json'
    """
    now = datetime.utcnow()
    return (
        f"players/"
        f"{now.year}/{now.month:02d}/{now.day:02d}/"
        f"players_{now.strftime('%Y%m%d_%H%M%S')}.json"
    )


def load_to_s3(data: list[dict]) -> str:
    """
    Uploads a list of player dicts to S3 as a JSON file.

    Args:
        data: clean list of player dicts from the transformer

    Returns:
        The S3 key where the file was saved
    """
    if not data:
        logger.warning("No data to upload — skipping S3 upload")
        return None

    s3_client = get_s3_client()
    s3_key = build_s3_key()

    # Convert to JSON string
    json_content = json.dumps(data, indent=2, ensure_ascii=False)

    logger.info(f"Uploading {len(data)} players to s3://{S3_BUCKET_NAME}/{s3_key}")

    s3_client.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=s3_key,
        Body=json_content.encode("utf-8"),
        ContentType="application/json",
    )

    logger.success(f"Successfully uploaded to s3://{S3_BUCKET_NAME}/{s3_key}")
    return s3_key