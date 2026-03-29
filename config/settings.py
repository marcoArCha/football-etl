import os
from dotenv import load_dotenv

load_dotenv()

# API
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
API_HOST = "v3.football.api-sports.io"

# AWS
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# Pipeline
SCHEDULE_HOURS = int(os.getenv("SCHEDULE_HOURS", 24))

# API endpoints
BASE_URL = "https://v3.football.api-sports.io"
LEAGUE_ID = 39   # Premier League
SEASON = 2024