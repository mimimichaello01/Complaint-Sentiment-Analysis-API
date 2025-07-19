from fastapi import Depends

from application.builders.complaint_builder import ComplaintBuilder
from application.enrichers.complaint_enricher import ComplaintEnricher
from application.interfaces.repositories.complaint_repository import AbstractComplaintRepository
from application.interfaces.services.complaint_service import AbstractComplaintService
from application.service.complaint_service_impl import ComplaintServiceImpl
from application.validators.complaint_validator import ComplaintValidator
from infra.db.db_halper import db_halper
from infra.http_clients.mistral_api_clients import MistralApiClient
from infra.http_clients.ip_api_client import GeoIPClient
from infra.http_clients.ninjas_api_client import ProfanityApiClient
from infra.http_clients.sentiment_api_client import SentimentApiClient
from infra.repositories.complaint_repository_impl import ComplaintRepositoryImpl

from settings.config import settings

def get_complaint_repository(
    db=Depends(db_halper.session_getter),
) -> AbstractComplaintRepository:
    return ComplaintRepositoryImpl(db)


def get_sentiment_client() -> SentimentApiClient:
    return SentimentApiClient()


def get_profanity_client() -> ProfanityApiClient:
    return ProfanityApiClient()


def get_geo_ip_client() -> GeoIPClient:
    return GeoIPClient()


def get_mistral_client() -> MistralApiClient:
    return MistralApiClient()


def get_complaint_validator(
    profanity_client: ProfanityApiClient = Depends(get_profanity_client),
) -> ComplaintValidator:
    return ComplaintValidator(profanity_client)


def get_complaint_builder(
    geo_ip_client: GeoIPClient = Depends(get_geo_ip_client),
) -> ComplaintBuilder:
    return ComplaintBuilder(geo_ip_client)


def get_complaint_enricher(
    sentiment_client: SentimentApiClient = Depends(get_sentiment_client),
    mistral_client: MistralApiClient = Depends(get_mistral_client),
) -> ComplaintEnricher:
    return ComplaintEnricher(sentiment_client, mistral_client)



def get_complaint_service(
    repo: AbstractComplaintRepository = Depends(get_complaint_repository),
    validator: ComplaintValidator = Depends(get_complaint_validator),
    builder: ComplaintBuilder = Depends(get_complaint_builder),
    enricher: ComplaintEnricher = Depends(get_complaint_enricher),
) -> AbstractComplaintService:
    return ComplaintServiceImpl(repo, validator, builder, enricher)
