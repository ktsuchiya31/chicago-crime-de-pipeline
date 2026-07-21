import boto3
import pandas as pd
import requests
import os
import logging
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def fetch_crimes(year: int = 2025, limit: int = 100000) -> pd.DataFrame:
    logger.info(f"Fetching crime data for year {year}")
    url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json"
    params = {
        "$where": f"year = {year}",
        "$limit": limit,
        "$order": "date DESC"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    df = pd.DataFrame(response.json())
    logger.info(f"Fetched {len(df)} records")
    return df

def clean_crimes(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Cleaning data")
    df = df.drop(columns=['location'], errors='ignore')
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df['x_coordinate'] = pd.to_numeric(df['x_coordinate'], errors='coerce')
    df['y_coordinate'] = pd.to_numeric(df['y_coordinate'], errors='coerce')
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.drop_duplicates(subset=['id'])
    logger.info(f"Cleaned data shape: {df.shape}")
    return df

def upload_to_s3(df: pd.DataFrame, bucket: str, key: str) -> None:
    logger.info(f"Uploading to s3://{bucket}/{key}")
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_DEFAULT_REGION')
    )
    csv_buffer = df.to_csv(index=False)
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=csv_buffer
    )
    logger.info("Upload complete")


def run():
    bucket = os.getenv('S3_BUCKET', 'chicago-crime-de-koutsuchiya')
    year = datetime.now().year
    df = fetch_crimes(year=year)
    df = clean_crimes(df)
    key = f"raw/crimes_{year}.csv"
    upload_to_s3(df, bucket, key)
    logger.info(f"Pipeline complete — {len(df)} rows uploaded to {key}")
    return {"row_count": len(df), "columns": list(df.columns)}


if __name__ == "__main__":
    run()