from celery import Celery

from settings.config import settings


celery_app = Celery(
    __name__,
    broker=settings.celery.broker_url,
    backend=settings.celery.result_backend
)

celery_app.conf.task_default_queue = 'emails'
celery_app.autodiscover_tasks(["infra.celery.tasks.complaint_tasks"])
