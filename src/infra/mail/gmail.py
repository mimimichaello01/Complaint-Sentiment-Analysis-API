import aiosmtplib
from email.message import EmailMessage
from pydantic import EmailStr
from infra.exceptions.mail import EmailSendException
from infra.mail.base import AbstractMailSender

from settings.config import GMailConfig

from logger.logger import setup_logger


logger = setup_logger(__name__)

class GMailSender(AbstractMailSender):
    def __init__(self, config: GMailConfig):
        self.host = config.host
        self.port = config.port
        self.username = config.username
        self.password = config.password
        self.from_email = config.mail_from
        self.use_tls = config.use_tls

    def _build_message(self, to: str, subject: str, body: str, html: bool = False) -> EmailMessage:
        msg = EmailMessage()
        msg["From"] = self.from_email
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body, subtype="html" if html else "plain")
        return msg

    async def send_mail(self, to: str, subject: str, body: str, *, html: bool = False):
        message = self._build_message(to, subject, body, html)
        try:
            await aiosmtplib.send(
                message,
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                use_tls=False,
                start_tls=True
            )
        except aiosmtplib.SMTPException as e:
            logger.exception("Ошибка при отправке письма через SMTP")
            raise EmailSendException()
