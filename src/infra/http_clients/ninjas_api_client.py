import httpx

from settings.config import settings

class ProfanityApiClient:
    def __init__(self):
        self.url = settings.api_ninjas.url
        self.api_key = settings.api_ninjas.key
        self.timeout = settings.api_ninjas.timeout

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
