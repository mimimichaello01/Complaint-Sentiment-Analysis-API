from infra.exceptions.base import BaseInfrastructureException


class SentimentApiUnavailableException(BaseInfrastructureException):
    def __init__(self, message: str = "Sentiment API is unavailable."):
        super().__init__(message, status_code=502)


class SentimentApiInternalException(BaseInfrastructureException):
    def __init__(self, message: str = "Sentiment API internal error."):
        super().__init__(message, status_code=502)


class ProfanityException(BaseInfrastructureException):
    def __init__(self, message: str = "Complaint text contains inappropriate language"):
        super().__init__(message, status_code=400)

class GeoIPNotFoundException(BaseInfrastructureException):
    def __init__(self, message: str = "Cannot resolve geo info "):
        super().__init__(message, status_code=400)
