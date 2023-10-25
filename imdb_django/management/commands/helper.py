import logging


# Initialize the logger
logger = logging.getLogger(__name__)

# Custom function to log detailed information
def log_info(header, data):
    logger.info(header)
    for key, value in data.items():
        logger.info(f"{key}: {value}")
