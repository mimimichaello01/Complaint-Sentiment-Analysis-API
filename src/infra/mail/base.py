from typing import Protocol

from pydantic import EmailStr

class AbstractMailSender(Protocol):
    async def send_mail(
        self,
        to: EmailStr,
        subject: str,
        body: str,
        *,
        html: bool = False
    ):
        ...
