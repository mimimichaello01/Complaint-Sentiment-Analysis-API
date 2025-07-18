import httpx

from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_exponential
from tenacity import retry_if_exception_type

from infra.exceptions.external_api import SentimentApiInternalException
from infra.exceptions.external_api import SentimentApiUnavailableException
from settings.config import settings


class SentimentApiClient:
    def __init__(self):
        self.url = settings.api_layer.url
        self.api_key = settings.api_layer.key
        self.timeout = settings.api_layer.timeout

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.NetworkError, httpx.HTTPStatusError, httpx.TimeoutException))
    )
    async def analyze(self, text: str) -> str:
        headers = {"apikey": self.api_key}

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                self.url,
                headers=headers,
                content=text,
            )
            response.raise_for_status()
            json_data = response.json()
            return json_data.get("sentiment", "unknown")
