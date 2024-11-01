import logging

from concurrent_log_handler import ConcurrentRotatingFileHandler


def setup_logging() -> logging.Logger:
    name = "RESTful_API_Logging"

    log_file_path = name + ".log"

    log_level = logging.DEBUG

    logger = logging.getLogger(name)
    # Ensure that the logger does not propagate messages to the root logger
    logger.propagate = False
    logger.setLevel(log_level)

    # Date format to match the desired format
    date_format = "%Y-%m-%dT%H:%M:%S"
    formatter = logging.Formatter(
        fmt="%(asctime)s.%(msecs)d - %(levelname)s - %(name)s - %(message)s", datefmt=date_format
    )

    # Use ConcurrentRotatingFileHandler for thread and process-safe file logging
    file_handler = ConcurrentRotatingFileHandler(
        str(log_file_path), mode="a", encoding="utf-8", maxBytes=49000000, backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


logger = setup_logging()
