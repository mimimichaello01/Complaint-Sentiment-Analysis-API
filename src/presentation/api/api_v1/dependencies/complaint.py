from fastapi import Depends

from application.service.complaint_service_impl import ComplaintServiceImpl
from infra.db.db_halper import db_halper
from infra.http_clients.ip_api_client import GeoIPClient
from infra.http_clients.ninjas_api_client import ProfanityApiClient
from infra.http_clients.sentiment_api_client import SentimentApiClient
from infra.repositories.complaint_repository_impl import ComplaintRepositoryImpl


def get_complaint_repository(
    db=Depends(db_halper.session_getter),
) -> ComplaintRepositoryImpl:
    return ComplaintRepositoryImpl(db)


def get_sentiment_client() -> SentimentApiClient:
    return SentimentApiClient()


def get_profanity_client() -> ProfanityApiClient:
    return ProfanityApiClient()

def get_geo_ip_client() -> GeoIPClient:
    return GeoIPClient()


def get_complaint_service(
    repo: ComplaintRepositoryImpl = Depends(get_complaint_repository),
    client: SentimentApiClient = Depends(get_sentiment_client),
    profanity: ProfanityApiClient = Depends(get_profanity_client),
    geo_ip_client: GeoIPClient = Depends(get_geo_ip_client),
) -> ComplaintServiceImpl:
    return ComplaintServiceImpl(repo, client, profanity, geo_ip_client)
