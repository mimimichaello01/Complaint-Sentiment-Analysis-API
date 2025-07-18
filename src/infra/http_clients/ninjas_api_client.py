import httpx

from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_exponential
from tenacity import retry_if_exception_type

from settings.config import settings

class ProfanityApiClient:
    def __init__(self):
        self.url = settings.api_ninjas.url
        self.api_key = settings.api_ninjas.key
        self.timeout = settings.api_ninjas.timeout

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.NetworkError, httpx.HTTPStatusError, httpx.TimeoutException))
    )
    async def check_profanity(self, text: str) -> bool:
        headers = {"X-Api-Key": self.api_key}
        params = {"text": text}

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                self.url,
                headers=headers,
                params=params,
            )

            response.raise_for_status()
            json_data = response.json()

            return json_data.get("has_profanity", False)
