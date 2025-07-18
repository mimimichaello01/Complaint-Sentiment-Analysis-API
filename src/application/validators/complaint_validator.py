from infra.exceptions.external_api import ProfanityException
from infra.http_clients.ninjas_api_client import ProfanityApiClient

from logger.logger import setup_logger


logger = setup_logger(__name__)

class ComplaintValidator:
    def __init__(self, profanity_client: ProfanityApiClient):
        self.profanity_client = profanity_client

    async def validate_text(self, text: str):
        if await self.profanity_client.check_profanity(text):
            logger.warning("Profanity detected in complaint text")
            raise ProfanityException()
