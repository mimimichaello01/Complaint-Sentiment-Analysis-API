from abc import ABC
from abc import abstractmethod
from typing import Optional
from uuid import UUID

from infra.models.complaints import Complaint


class AbstractComplaintRepository(ABC):
    @abstractmethod
    async def get_by_id(self, complaint_id: UUID) -> Optional[Complaint]:
        ...

    @abstractmethod
    async def create(self, complaint: Complaint) -> Complaint:
        ...
