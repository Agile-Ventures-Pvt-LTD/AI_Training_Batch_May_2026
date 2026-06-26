import logging

import config

config.LOG_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

logging.basicConfig(
    filename=config.LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)