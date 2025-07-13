from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from infra.models.complaints import Category, Sentiment, Status


class ComplaintResponseSchema(BaseModel):
    id: UUID
    text: str
    status: Status
    sentiment: Sentiment
    category: Category
    ip: str
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    created_at: datetime
