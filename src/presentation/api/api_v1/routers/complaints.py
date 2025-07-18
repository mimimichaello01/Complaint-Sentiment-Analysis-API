from fastapi import APIRouter, Depends, Request

from settings.config import settings

from application.dto.complaints import ComplaintCreateDTO
from application.schemas.complaints import ComplaintResponseSchema

from application.service.complaint_service_impl import ComplaintServiceImpl

from presentation.api.api_v1.dependencies.complaint import get_complaint_service


complaint_router = APIRouter(prefix=settings.api_prefix.complaint.prefix, tags=["Complaint"])


@complaint_router.post("/add", response_model=ComplaintResponseSchema)
async def create_complaint(
    data: ComplaintCreateDTO,
    request: Request,
    service: ComplaintServiceImpl = Depends(get_complaint_service)
):
    ip_address = service.builder.geo_ip_client.get_ip(request)
    return await service.create_complaint(data, ip_address)
