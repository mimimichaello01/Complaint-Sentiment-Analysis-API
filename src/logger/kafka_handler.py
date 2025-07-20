from datetime import datetime
import json
import logging
from logging import Handler
import traceback
from kafka import KafkaProducer

class KafkaLoggingHandler(Handler):
    def __init__(self, bootstrap_servers: str, topic: str):
        super().__init__()
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.producer = None

    def emit(self, record: logging.LogRecord):
        try:
            if not self.producer:
                self.producer = KafkaProducer(
                    bootstrap_servers=self.bootstrap_servers.split(","),
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    retries=5,
                )

            log_entry = self.format(record)
            message = {
                "level": record.levelname,
                "logger": record.name,
                "message": log_entry,
                "time": datetime.now().isoformat(),
                "pathname": record.pathname,
                "lineno": record.lineno,
                "funcName": record.funcName,
            }
            self.producer.send(self.topic, value=message)

        except Exception:
            print(traceback.format_exc())
            self.handleError(record)
