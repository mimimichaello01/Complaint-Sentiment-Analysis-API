class BaseApplicationException(Exception):
    """
    Базовое исключение для бизнес-логики приложения.
    """
    def __init__(self, message: str = "Application error.", status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)
