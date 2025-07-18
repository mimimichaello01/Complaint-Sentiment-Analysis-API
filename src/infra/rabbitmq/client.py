import aio_pika
from settings.config import RabbitMQConfig, settings
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError


class RabbitMQClient:
    """
    Клиент для работы с RabbitMQ.
    """

    def __init__(self, config: RabbitMQConfig = settings.rabbitmq):
        self.config = config
        self.connection = None
        self.channel = None
        self.exchange = None

    @retry(
        stop=stop_after_attempt(10), wait=wait_exponential(multiplier=1), reraise=True
    )
    async def connect(self):
        self.connection = await aio_pika.connect_robust(
            host=self.config.host,
            port=self.config.port,
            login=self.config.user,
            password=self.config.password,
        )

        self.channel = await self.connection.channel()
