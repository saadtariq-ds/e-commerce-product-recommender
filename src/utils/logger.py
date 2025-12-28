"""
Application Logging Configuration

This module configures centralized logging for the application.
It creates a timestamped log file and provides a helper function
to retrieve named loggers.
"""

import os
import logging
from datetime import datetime

# Generate a timestamped log file name
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Create logs directory path (logs/<timestamp>.log)
LOGS_PATH = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(LOGS_PATH, exist_ok=True)

# Full path to the log file
LOG_FILE_PATH = os.path.join(LOGS_PATH, LOG_FILE)

# Configure the global logging settings
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def get_logger(name: str) -> logging.Logger:
    """
    Retrieve a configured logger instance.

    Args:
        name (str): Name of the logger (typically __name__).

    Returns:
        logging.Logger: Logger instance configured with INFO level.
    """

    # Create or retrieve the logger
    logger = logging.getLogger(name)

    # Set logging level
    logger.setLevel(logging.INFO)

    return logger