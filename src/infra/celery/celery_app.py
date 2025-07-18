from celery import Celery

from settings.config import settings


celery_app = Celery(
    __name__,
    broker=settings.celery.broker_url,
    backend=settings.celery.result_backend
)
