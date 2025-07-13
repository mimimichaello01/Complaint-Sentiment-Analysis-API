from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from application.exceptions.base import BaseApplicationException
from infra.exceptions.base import BaseInfrastructureException


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(BaseApplicationException)
    async def base_app_exception_handler(request: Request, exc: BaseApplicationException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message}
        )

    @app.exception_handler(BaseInfrastructureException)
    async def base_infra_exception_handler(request: Request, exc: BaseInfrastructureException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message}
        )
