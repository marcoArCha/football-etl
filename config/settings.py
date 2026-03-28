import os
from dotenv import load_dotenv

load_dotenv()

# API
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "api-football-v1.p.rapidapi.com"

# AWS
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# Pipeline
SCHEDULE_HOURS = int(os.getenv("SCHEDULE_HOURS", 24))

# API endpoints
BASE_URL = "https://api-football-v1.p.rapidapi.com/v3"
LEAGUE_ID = 39   # Premier League
SEASON = 2024