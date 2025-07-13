import httpx
from infra.exceptions.external_api import SentimentApiInternalException, SentimentApiUnavailableException
from settings.config import settings


class SentimentApiClient:
    def __init__(self):
        self.url = settings.api_layer.url
        self.api_key = settings.api_layer.key
        self.timeout = settings.api_layer.timeout

    async def analyze(self, text: str) -> str:
        headers = {"apikey": self.api_key}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.url,
                    headers=headers,
                    content=text,
                )
                response.raise_for_status()
                json_data = response.json()
                return json_data.get("sentiment", "unknown")

        except (httpx.RequestError, httpx.TimeoutException) as e:
            raise SentimentApiUnavailableException() from e

        except httpx.HTTPStatusError as e:
            if 500 <= e.response.status_code < 600:
                raise SentimentApiInternalException() from e
            raise SentimentApiInternalException("Unexpected HTTP status.") from e

        except Exception as e:
            raise SentimentApiInternalException("Unexpected error") from e
