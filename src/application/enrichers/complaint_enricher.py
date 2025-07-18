from infra.exceptions.external_api import SentimentApiUnavailableException
from infra.http_clients.mistral_api_clients import MistralApiClient
from infra.http_clients.sentiment_api_client import SentimentApiClient
from infra.models.complaints import Category, Complaint, Sentiment
from infra.mappers.sentiment_mapper import map_external_sentiment


from logger.logger import setup_logger


logger = setup_logger(__name__)


class ComplaintEnricher:
    def __init__(
        self, sentiment_client: SentimentApiClient, mistral_client: MistralApiClient
    ):
        self.sentiment_client = sentiment_client
        self.mistral_client = mistral_client

    async def enrich(self, complaint: Complaint) -> None:
        complaint.sentiment = await self._analyze_sentiment(complaint.text)
        complaint.category = await self._predict_category(complaint.text)

    async def _analyze_sentiment(self, text: str) -> Sentiment:
        try:
            raw = await self.sentiment_client.analyze(text)
            return map_external_sentiment(raw)
        except SentimentApiUnavailableException:
            logger.warning("Sentiment API unavailable. Using default 'unknown'.")
            return Sentiment.UNKNOWN

    async def _predict_category(self, text: str) -> Category:
        try:
            return await self.mistral_client.get_category(text)
        except Exception as e:
            logger.warning(f"Failed to get category from AI: {e}")
            return Category.OTHER
