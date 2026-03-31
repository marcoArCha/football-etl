# ⚽ Football ETL Pipeline

A production-style ETL pipeline that extracts Premier League player data from the API-Football API, transforms and cleans it, and loads it to AWS S3 as partitioned JSON files.

Built with Python, Docker, and AWS — designed to run on a schedule in a containerized environment.

---

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────────┐
│                   Docker Container                   │
│                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────────┐  │
│  │ Extract  │───▶│Transform │───▶│    Load      │  │
│  │  (API)   │    │ (Pandas) │    │  (AWS S3)    │  │
│  └──────────┘    └──────────┘    └──────────────┘  │
│                                                     │
│              APScheduler (every 24 hours)           │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │     AWS S3 Bucket   │
              │  players/           │
              │  └── 2026/03/30/    │
              │      └── data.json  │
              └─────────────────────┘
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Core language |
| Requests | HTTP API calls |
| Pandas | Data transformation and cleaning |
| Boto3 | AWS S3 client |
| APScheduler | Pipeline scheduling |
| Loguru | Structured logging |
| Docker | Containerization |
| AWS S3 | Data lake storage |
| AWS EC2 | Production deployment |

---

## 📁 Project Structure
```
football-etl/
├── src/
│   ├── extractors/
│   │   ├── players_extractor.py      # Fetches players from API
│   │   └── stats_extractor.py        # Fetches player statistics
│   ├── transformers/
│   │   └── merge_transformer.py      # Flattens and cleans data
│   ├── loaders/
│   │   └── s3_loader.py              # Uploads JSON to S3
│   └── pipeline.py                   # Orchestrates the ETL flow
├── config/
│   └── settings.py                   # Centralized configuration
├── tests/
│   └── test_pipeline.py              # Unit tests
├── .env.example                      # Environment variables template
├── Dockerfile                        # Container definition
├── docker-compose.yml                # Container orchestration
├── requirements.txt                  # Python dependencies
└── README.md                         # You are here
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- AWS account with S3 access
- API-Football account (free tier)

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/football-etl.git
cd football-etl
```

### 2. Set up environment variables
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
RAPIDAPI_KEY=your_api_football_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your_bucket_name
SCHEDULE_HOURS=24
```

### 3. Run locally with Docker
```bash
docker compose up -d
```

### 4. Check logs
```bash
docker compose logs -f
```

---

## 📊 Data Output

Each pipeline run produces a JSON file in S3 with the following structure:
```json
[
  {
    "player_id": 19073,
    "name": "B. Godfrey",
    "age": 27,
    "nationality": "England",
    "position": "Defender",
    "team": "Ipswich",
    "appearances": 11,
    "minutes_played": 159,
    "rating": 6.1,
    "goals": null,
    "assists": 0,
    "pass_accuracy": null,
    "key_passes": null,
    "tackles": 1,
    "interceptions": 2,
    "duels_total": 6,
    "duels_won": 4,
    "yellow_cards": 1,
    "red_cards": 0
  }
]
```

Files are partitioned by date:
```
s3://your-bucket/players/2026/03/30/players_20260330_231919.json
```

---

## ☁️ Production Deployment (AWS EC2)

See [deployment instructions](#) for step-by-step guide to deploy on an EC2 `t2.micro` instance (AWS Free Tier).

---

## 🔒 Security

- AWS credentials are never hardcoded — loaded from environment variables
- `.env` file is excluded from version control via `.gitignore`
- IAM user follows the Principle of Least Privilege (S3 access only)
- Docker image does not contain any secrets

---

## 🗺️ Future Improvements

- [ ] Replace `AmazonS3FullAccess` with a custom IAM policy scoped to a single bucket
- [ ] Use AWS Secrets Manager instead of `.env` for secret management
- [ ] Use IAM Roles instead of access keys for EC2 deployment
- [ ] Make league and season configurable via CLI arguments
- [ ] Add data validation with Great Expectations or Pydantic
- [ ] Store data in Parquet format instead of JSON for better query performance
- [ ] Add unit tests with pytest and mock API responses
- [ ] Set up CI/CD with GitHub Actions
- [ ] Add automatic season detection based on current date

---

## 📄 License

MIT