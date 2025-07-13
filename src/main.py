from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import Request

from fastapi.responses import JSONResponse

from contextlib import asynccontextmanager

from exceptions.exception_handlers import register_exception_handlers

from settings.config import settings
from infra.db import db_halper

from presentation.api.api_v1.routers.complaints import complaint_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startapp
    yield
    # shutdown
    await db_halper.dispose()


api_router = APIRouter(prefix=settings.api_prefix.prefix)

api_router.include_router(complaint_router)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Complaints",
        docs_url="/api/docs",
        debug=True,
        lifespan=lifespan,
    )

    # Регистрация кастомного обработчика исключений
    register_exception_handlers(app)

    app.include_router(api_router)
    return app
