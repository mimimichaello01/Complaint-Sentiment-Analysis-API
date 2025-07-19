import os

from pydantic import BaseModel
from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggerConfig(BaseModel):
    level: str = "INFO"
    format: str = (
        "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
    )
    log_to_file: bool = True
    max_bytes: int = 10 * 1024 * 1024
    backup_count: int = 5
    datefmt: str = "%Y-%m-%d %H:%M:%S"


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ComplaintApiPrefix(BaseModel):
    prefix: str = "/complaint"


class ApiPrefix(BaseModel):
    prefix: str = "/api/v1"
    complaint: ComplaintApiPrefix = ComplaintApiPrefix()


class DatabaseConfig(BaseModel):
    url: AnyUrl
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class ApiLayerConfig(BaseModel):
    key: str
    url: str
    timeout: float = 30.0

class ApiNinjasConfig(BaseModel):
    key: str
    url: str
    timeout: float = 30.0

class ApiIpConfig(BaseModel):
    url: str
    timeout: float = 5.0

class ApiMistralConfig(BaseModel):
    key: str
    url: str
    timeout: float = 30.0


class RabbitMQConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str


class CeleryConfig(BaseModel):
    broker_url: str
    result_backend: str


class RedisSettings(BaseModel):
    host: str
    port: int
    db: int

class GMailConfig(BaseModel):
    username: str
    password: str
    host: str
    port: int
    mail_from: str
    use_tls: bool
    notification_email: str  

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.dev",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    api_prefix: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    logger: LoggerConfig = LoggerConfig()
    api_layer: ApiLayerConfig
    api_ninjas: ApiNinjasConfig
    api_ip: ApiIpConfig
    api_mistral: ApiMistralConfig
    rabbitmq: RabbitMQConfig
    celery: CeleryConfig
    redis: RedisSettings
    gmail: GMailConfig

settings = Settings()  # type: ignore
