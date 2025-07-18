from abc import ABC
from abc import abstractmethod
from typing import Optional
from uuid import UUID

from infra.models.complaints import Complaint
from application.dto.complaints import ComplaintCreateDTO


class AbstractComplaintService(ABC):
    @abstractmethod
    async def get_complaint_by_id(self, complaint_id: UUID) -> Optional[Complaint]:
        ...

    @abstractmethod
    async def create_complaint(self, data: ComplaintCreateDTO, ip_address: str) -> Complaint:
        ...
