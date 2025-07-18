from infra.exceptions.base import BaseInfrastructureException


class EmailSendException(BaseInfrastructureException):
    def __init__(self, message: str = "Error sending email"):
        super().__init__(message, status_code=400)
