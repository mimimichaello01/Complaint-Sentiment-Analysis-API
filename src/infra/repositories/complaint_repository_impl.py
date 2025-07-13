from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from application.interfaces.repositories.complaint_repository import (
    AbstractComplaintRepository,
)
from infra.models.complaints import Complaint


class ComplaintRepositoryImpl(AbstractComplaintRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, complaint_id: UUID) -> Optional[Complaint]:
        return await self.session.get(Complaint, complaint_id)

    async def create(self, complaint: Complaint) -> Complaint:
        self.session.add(complaint)
        await self.session.flush()
        return complaint
