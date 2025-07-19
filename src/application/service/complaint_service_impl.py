from uuid import UUID

from typing import Optional

from application.builders.complaint_builder import ComplaintBuilder
from application.dto.complaints import ComplaintCreateDTO

from application.enrichers.complaint_enricher import ComplaintEnricher
from application.interfaces.repositories.complaint_repository import (
    AbstractComplaintRepository,
)
from application.interfaces.services.complaint_service import AbstractComplaintService
from application.validators.complaint_validator import ComplaintValidator


from application.exceptions.complaint import ComplaintNotFoundException


from infra.celery.tasks.complaint_tasks import send_complaint_email_task
from infra.models.complaints import Complaint


from logger.logger import setup_logger


logger = setup_logger(__name__)


class ComplaintServiceImpl(AbstractComplaintService):
    def __init__(
        self,
        complaint_repo: AbstractComplaintRepository,
        validator: ComplaintValidator,
        builder: ComplaintBuilder,
        enricher: ComplaintEnricher,
    ):
        self.complaint_repo = complaint_repo
        self.validator = validator
        self.builder = builder
        self.enricher = enricher

    async def get_complaint_by_id(self, complaint_id: UUID) -> Optional[Complaint]:
        complaint = await self.complaint_repo.get_by_id(complaint_id)
        if not complaint:
            logger.info(f"Complaint not found: {complaint_id}")
            raise ComplaintNotFoundException()
        logger.debug(f"Complaint fetched: {complaint.id}")
        return complaint

    async def create_complaint(
        self, data: ComplaintCreateDTO, ip_address: str
    ) -> Complaint:
        logger.debug(f"Received complaint: {data.text}")

        await self.validator.validate_text(data.text)

        complaint = await self.builder.build_initial(data.text, ip_address)

        await self.enricher.enrich(complaint)

        await self.complaint_repo.create(complaint)

        if complaint.category == "Technical":
            send_complaint_email_task.apply_async(args=[complaint.id, complaint.text, complaint.category], queue='emails')

        logger.info(f"Complaint created: {complaint.id}")
        return complaint
