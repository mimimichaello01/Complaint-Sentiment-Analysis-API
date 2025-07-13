class BaseInfrastructureException(Exception):
    """
    Базовое исключение для инфраструктуры.
    """
    def __init__(self, message: str = "Infrastructure error.", status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)
