"""
Base domain models shared across all planes.
Every tenant-scoped domain object inherits from TenantScopedModel.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Generic, TypeVar
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class TenantScopedModel(BaseModel):
    """
    Base model for all tenant-scoped domain objects.
    These fields are invariants — they cannot be removed or renamed
    without a platform-level breaking change and a new major version.
    """
    id: UUID = Field(default_factory=uuid4)
    tenant_id: UUID
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
    created_by: str | None = None
    updated_by: str | None = None

    class Config:
        from_attributes = True


class PlatformEvent(BaseModel):
    """
    CloudEvents 1.0 compatible event envelope.
    All events emitted by any plane must use this structure.

    Event type format: kop.{plane}.{entity}.{action}.v{version}
    Example: kop.ingestion.document.created.v1
    """
    id: UUID = Field(default_factory=uuid4)
    specversion: str = "1.0"
    type: str
    source: str
    subject: str
    tenant_id: UUID
    time: datetime = Field(default_factory=utcnow)
    data: dict
    datacontenttype: str = "application/json"


T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    data: T
    request_id: str
    timestamp: datetime = Field(default_factory=utcnow)


class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: dict | None = None
    request_id: str
    timestamp: datetime = Field(default_factory=utcnow)


class PaginatedResponse(BaseModel, Generic[T]):
    data: list[T]
    total: int
    page: int = 1
    page_size: int = 20
    has_next: bool = False
    cursor: str | None = None
    request_id: str
    timestamp: datetime = Field(default_factory=utcnow)
