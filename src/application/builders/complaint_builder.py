from uuid import uuid4

from infra.exceptions.external_api import GeoIPNotFoundException

from infra.http_clients.ip_api_client import GeoIPClient

from infra.models.complaints import Category, Complaint, Sentiment, Status


from logger.logger import setup_logger


logger = setup_logger(__name__)

class ComplaintBuilder:
    def __init__(self, geo_ip_client: GeoIPClient):
        self.geo_ip_client = geo_ip_client

    async def build_initial(self, text: str, ip: str) -> Complaint:
        try:
            geo = await self.geo_ip_client.get_geo_data(ip)
        except GeoIPNotFoundException:
            logger.warning(f"GeoIP lookup failed for IP: {ip}")
            geo = {"ip": ip, "country": None, "region": None, "city": None}

        return Complaint(
            id=uuid4(),
            text=text,
            status=Status.OPEN,
            sentiment=Sentiment.UNKNOWN,
            category=Category.OTHER,
            ip=geo["ip"],
            country=geo["country"],
            region=geo["region"],
            city=geo["city"],
        )
