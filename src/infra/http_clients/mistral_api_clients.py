import httpx

from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_exponential
from tenacity import retry_if_exception_type

from infra.models.complaints import Category
from settings.config import settings


class MistralApiClient:
    def __init__(self):
        self.url = settings.api_mistral.url
        self.key = settings.api_mistral.key
        self.timeout = settings.api_mistral.timeout

    def _build_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
        }

    def _build_prompt(self, complaint_text: str) -> str:
        return (
            f'Определи категорию жалобы: "{complaint_text}". '
            f"Варианты: TECHNICAL, PAYMENT, OTHER. Ответ только одним словом."
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.NetworkError, httpx.HTTPStatusError, httpx.TimeoutException))
    )
    async def get_category(self, complaint_text: str) -> Category:
        payload = {
            "model": "mistral-tiny",
            "messages": [
                {"role": "user", "content": self._build_prompt(complaint_text)}
            ],
            "temperature": 0.7,
            "max_tokens": 10,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                self.url, headers=self._build_headers(), json=payload
            )

            response.raise_for_status()
            json_data = response.json()

            category_map = {
                "TECHNICAL": Category.TECHNICAL,
                "PAYMENT": Category.PAYMENT,
                "OTHER": Category.OTHER,
            }

            raw = json_data["choices"][0]["message"]["content"].strip().upper()
            return category_map.get(raw, Category.OTHER)
