from application.exceptions.base import BaseApplicationException


class ComplaintNotFoundException(BaseApplicationException):
    def __init__(self, message: str = "Complaint with this ID not found."):
        super().__init__(message, status_code=404)
