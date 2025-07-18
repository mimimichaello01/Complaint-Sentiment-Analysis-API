import json
import aio_pika

from typing import Any

from infra.rabbitmq.client import RabbitMQClient
from logger.logger import setup_logger


logger = setup_logger(__name__)


class PublisherRabbitMQ(RabbitMQClient):
    """
    Клиент для отправки сообщений в RabbitMQ.
    """

    async def publisher(
        self,
        message: Any,
        exchange_name: str,
        routing_key: str,
        exchange_type: aio_pika.ExchangeType = aio_pika.ExchangeType.DIRECT
        ):
        if not self.channel:
            raise Exception("Канал RabbitMQ не открыт")

        try:
            if isinstance(message, str):
                body = message.encode()
            else:
                body = json.dumps(message).encode()

            exchange = await self.channel.declare_exchange(
                name=exchange_name,
                type=exchange_type,
                durable=True,
            )

            await exchange.publish(
                aio_pika.Message(body=body),
                routing_key=routing_key,
            )

            logger.info(f"Сообщение отправлено: exchange={exchange_name}, key={routing_key}")

        except Exception as e:
            logger.error(f"Ошибка при отправке в RabbitMQ: {e}")
            raise
