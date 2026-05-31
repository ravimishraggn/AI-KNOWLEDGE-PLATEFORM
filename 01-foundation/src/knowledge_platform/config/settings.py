"""
Platform-wide configuration model.
All configuration is sourced from environment variables.
"""
from __future__ import annotations

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    url: str = Field(..., alias="KOP_DB_URL")
    pool_size: int = Field(10, alias="KOP_DB_POOL_SIZE")
    max_overflow: int = Field(20, alias="KOP_DB_MAX_OVERFLOW")
    echo: bool = Field(False, alias="KOP_DB_ECHO")


class RedisConfig(BaseSettings):
    url: str = Field("redis://localhost:6379", alias="KOP_REDIS_URL")
    max_connections: int = Field(50, alias="KOP_REDIS_MAX_CONNECTIONS")


class AuthConfig(BaseSettings):
    provider: str = Field("jwt", alias="KOP_AUTH_PROVIDER")
    secret_key: SecretStr = Field(..., alias="KOP_SECRET_KEY")
    algorithm: str = Field("RS256", alias="KOP_AUTH_ALGORITHM")
    access_token_expire_minutes: int = Field(30, alias="KOP_TOKEN_EXPIRE_MINUTES")


class StorageConfig(BaseSettings):
    adapter: str = Field("s3", alias="KOP_STORAGE_ADAPTER")
    bucket: str = Field(..., alias="KOP_STORAGE_BUCKET")
    region: str = Field("us-east-1", alias="KOP_STORAGE_REGION")


class EventBusConfig(BaseSettings):
    adapter: str = Field("redis_streams", alias="KOP_EVENT_BUS_ADAPTER")
    stream_prefix: str = Field("kop", alias="KOP_STREAM_PREFIX")


class PlatformSettings(BaseSettings):
    env: str = Field("development", alias="KOP_ENV")
    debug: bool = Field(False, alias="KOP_DEBUG")
    enable_docs: bool = Field(True, alias="KOP_ENABLE_DOCS")
    cors_origins: list[str] = Field(["*"], alias="KOP_CORS_ORIGINS")
    tenant_mode: str = Field("multi", alias="KOP_TENANT_MODE")
    plugin_scan: bool = Field(True, alias="KOP_PLUGIN_SCAN")

    # Nested configs — each reads its own env vars
    # These are initialized separately and injected
    # to avoid circular env var resolution

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
