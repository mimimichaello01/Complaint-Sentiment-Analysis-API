from logging.handlers import RotatingFileHandler
import os
import sys
import logging
from logger.kafka_handler import KafkaLoggingHandler
from settings.config import settings


def setup_logger(name: str = "app") -> logging.Logger:
    """
    Setup logger
    """
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(settings.logger.level)
    # create formatter
    formatter = logging.Formatter(
        fmt=settings.logger.format, datefmt=settings.logger.datefmt
    )

    # Stream to stdout
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    #File handler with rotation
    if settings.logger.log_to_file:
        log_file = "logs/app.log"
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=settings.logger.max_bytes,
            backupCount=settings.logger.backup_count,
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if settings.logger.log_to_kafka:

        kafka_handler = KafkaLoggingHandler(
            topic=settings.logger.kafka_topic,
            bootstrap_servers=settings.logger.kafka_bootstrap_servers
        )
        kafka_handler.setFormatter(formatter)
        logger.addHandler(kafka_handler)

    return logger
