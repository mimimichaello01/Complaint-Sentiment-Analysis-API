import httpx

from fastapi import Request

from infra.exceptions.external_api import GeoIPNotFoundException
from settings.config import settings


class GeoIPClient:
    def __init__(self):
        self.url = settings.api_ip.url
        self.timeout = settings.api_ip.timeout

    def get_ip(self, request: Request) -> str:
        x_forwarded_for = request.headers.get("X-Forwarded-For")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()

        client = request.client
        if client and client.host:
            return client.host

        raise GeoIPNotFoundException("Unable to determine client IP address")

    async def get_geo_data(self, ip: str) -> dict:
        params = {"ip": ip}

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                self.url,
                params=params,
            )

            response.raise_for_status()
            json_data = response.json()

            if json_data.get("status") != "success":
                raise GeoIPNotFoundException(f"Cannot resolve geo info for IP: {ip}")

            return {
                "ip": ip,
                "country": json_data.get("country"),
                "region": json_data.get("regionName"),
                "city": json_data.get("city"),
            }
