import sys
from loguru import logger


def setup_logger() -> None:
    """
    Configure loguru logger for console and file outputs.
    - Console: human-readable format
    - File: daily rotation, 7 days retention
    """
    logger.remove()  # Remove default logger to avoid duplicate logs

    # Console logging
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level}</level> | "
               "{name}:{function}:{line} - {message}",
        level="INFO",
    )

    # File logging
    logger.add(
        "../logs/bot.log",
        rotation="1 day",
        retention="7 days",
        encoding="utf-8",
        enqueue=True,  # Thread-safe logging
        backtrace=True,  # Show full traceback
        diagnose=True,  # More detailed exception info
    )
