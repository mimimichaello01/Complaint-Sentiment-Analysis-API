from uuid import UUID, uuid4

from typing import Optional

from application.dto.complaints import ComplaintCreateDTO

from application.interfaces.services.complaint_service import AbstractComplaintService
from infra.http_clients.ip_api_client import GeoIPClient
from infra.repositories.complaint_repository_impl import ComplaintRepositoryImpl

from infra.http_clients.sentiment_api_client import SentimentApiClient
from infra.http_clients.ninjas_api_client import ProfanityApiClient

from application.exceptions.complaint import ComplaintNotFoundException
from infra.exceptions.external_api import (
    GeoIPNotFoundException,
    ProfanityException,
    SentimentApiUnavailableException,
)

from infra.models.complaints import Category, Complaint, Sentiment, Status

from infra.mappers.sentiment_mapper import map_external_sentiment

from logger.logger import setup_logger


logger = setup_logger(__name__)


class ComplaintServiceImpl(AbstractComplaintService):
    def __init__(
        self,
        complaint_repo: ComplaintRepositoryImpl,
        sentiment_client: SentimentApiClient,
        profanity_client: ProfanityApiClient,
        geo_ip_client: GeoIPClient,
    ):
        self.complaint_repo = complaint_repo
        self.sentiment_client = sentiment_client
        self.profanity_client = profanity_client
        self.geo_ip_client = geo_ip_client

    async def get_complaint_by_id(self, complaint_id: UUID) -> Optional[Complaint]:
        complaint = await self.complaint_repo.get_by_id(complaint_id)
        if not complaint:
            logger.info(f"Complaint not found: {complaint_id}")
            raise ComplaintNotFoundException()
        logger.debug(f"Complaint fetched: {complaint.id}")
        return complaint

    async def create_complaint(self, data: ComplaintCreateDTO, ip_address: str) -> Complaint:
        logger.debug(f"Received create_complaint request with text: {data.text}")

        profanity_check = await self.profanity_client.check_profanity(data.text)
        if profanity_check:
            logger.warning("Profanity detected in complaint text")
            raise ProfanityException()

        try:
            geo_data = await self.geo_ip_client.get_geo_data(ip_address)
        except GeoIPNotFoundException:
            logger.warning(f"GeoIP lookup failed for IP: {ip_address}")
            geo_data = {
                "ip": ip_address,
                "country": None,
                "region": None,
                "city": None,
            }

        complaint = Complaint(
            id=uuid4(),
            text=data.text,
            status=Status.OPEN,
            sentiment=Sentiment.UNKNOWN,
            category=Category.OTHER,
            ip=geo_data["ip"],
            country=geo_data["country"],
            region=geo_data["region"],
            city=geo_data["city"],
        )
        logger.debug(f"Creating complaint: {complaint.id}")

        try:
            sentiment = await self.sentiment_client.analyze(complaint.text)
            logger.debug(f"Sentiment analyzed: {sentiment}")

        except SentimentApiUnavailableException:
            logger.warning("Sentiment API unavailable. Using default 'unknown'.")
            sentiment = "unknown"

        complaint.sentiment = map_external_sentiment(sentiment)

        await self.complaint_repo.create(complaint)
        await self.complaint_repo.session.commit()
        await self.complaint_repo.session.refresh(complaint)

        logger.info(
            f"Complaint created: {complaint.id}, sentiment: {complaint.sentiment}, "
            f"IP: {complaint.ip}, Country: {complaint.country}, City: {complaint.city}"
        )
        return complaint
