import logging
import schedule
import time
from app.main import run_pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

schedule.every(30).minutes.do(run_pipeline)

while True:
    try:
        schedule.run_pending()
    except Exception as exc:
        logger.error("Scheduler error: %s", exc)
    time.sleep(1)
