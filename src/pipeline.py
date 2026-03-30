import sys
from loguru import logger
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

from src.extractors.players_extractor import extract_all_players
from src.transformers.merge_transformer import transform
from src.loaders.s3_loader import load_to_s3
from config.settings import SCHEDULE_HOURS

# Configure logger — prints to console AND saves to file
logger.remove()  # Remove default handler
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
)
logger.add(
    "logs/pipeline.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="1 day",
    retention="7 days",
)


def run_pipeline():
    """
    Main ETL pipeline function.
    Extract → Transform → Load
    """
    logger.info("=" * 50)
    logger.info(f"Pipeline started at {datetime.utcnow()} UTC")
    logger.info("=" * 50)

    try:
        # Step 1 — Extract
        logger.info("Step 1/3 — Extracting players from API...")
        players_raw = extract_all_players()

        if not players_raw:
            logger.error("No players extracted — aborting pipeline")
            return

        # Step 2 — Transform
        logger.info("Step 2/3 — Transforming data...")
        players_clean = transform(players_raw)

        if not players_clean:
            logger.error("No players after transformation — aborting pipeline")
            return

        # Step 3 — Load
        logger.info("Step 3/3 — Loading to S3...")
        s3_key = load_to_s3(players_clean)

        logger.info("=" * 50)
        logger.success(f"Pipeline completed successfully!")
        logger.success(f"Players processed: {len(players_clean)}")
        logger.success(f"File saved at: s3://football-etl-data/{s3_key}")
        logger.info("=" * 50)

    except Exception as e:
        logger.error(f"Pipeline failed with error: {e}")
        raise


def main():
    """
    Entry point — runs the pipeline once immediately,
    then schedules it to run every X hours.
    """
    logger.info(f"Starting Football ETL — scheduled every {SCHEDULE_HOURS} hours")

    # Run once immediately on startup
    run_pipeline()

    # Then schedule it
    scheduler = BlockingScheduler()
    scheduler.add_job(
        run_pipeline,
        trigger="interval",
        hours=SCHEDULE_HOURS,
        id="football_etl_pipeline",
    )

    logger.info(f"Scheduler started — next run in {SCHEDULE_HOURS} hours")

    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Pipeline stopped manually")
        scheduler.shutdown()


if __name__ == "__main__":
    main()