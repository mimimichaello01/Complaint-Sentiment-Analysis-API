import asyncio

from infra.celery import celery_app
from infra.exceptions.mail import EmailSendException
from infra.mail.base import AbstractMailSender
from infra.mail.gmail import GMailSender
from settings.config import settings

from logger.logger import setup_logger


logger = setup_logger(__name__)


async def send_complaint_notification(
    complaint_id: str,
    complaint_text: str,
    complaint_category: str,
    gmail_sender: AbstractMailSender,
):
    body = (
        f"Поступила новая жалоба:\n\n"
        f"ID: {complaint_id}\n"
        f"Категория: {complaint_category}\n"
        f"Текст жалобы: {complaint_text}\n"
    )

    try:
        await gmail_sender.send_mail(
            to="your-mail@.com",
            subject="Новая жалоба создана",
            body=body,
            html=False,
        )
        logger.info(f"Уведомление по жалобе {complaint_id} успешно отправлено.")
    except EmailSendException as e:
        logger.error(f"Ошибка при отправке email для жалобы {complaint_id}: {e}")


@celery_app.task(
    bind=True, name="send_complaint_email_task", max_retries=3, default_retry_delay=10
)
def send_complaint_email_task(
    self, complaint_id: str, complaint_text: str, complaint_category: str
):
    sender = GMailSender(settings.gmail)
    asyncio.run(
        send_complaint_notification(
            complaint_id, complaint_text, complaint_category, sender
        )
    )
