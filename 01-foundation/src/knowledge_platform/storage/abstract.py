"""
Cloud-neutral object storage interface.
Implement this ABC to support a new storage backend.

Register via entry point:
    [project.entry-points."kop.storage"]
    my_backend = "my_package:MyStorageAdapter"
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class StorageObject:
    key: str
    size: int
    content_type: str | None
    last_modified: datetime
    metadata: dict


class StorageInterface(ABC):
    """
    Vendor-neutral object storage abstraction.
    All platform reads/writes go through this interface.
    """

    @abstractmethod
    async def put(
        self,
        key: str,
        data: bytes,
        content_type: str | None = None,
        metadata: dict | None = None,
    ) -> StorageObject:
        """Upload an object. Creates or overwrites."""
        ...

    @abstractmethod
    async def get(self, key: str) -> bytes:
        """
        Download an object by key.
        Raises ObjectNotFoundError if key does not exist.
        """
        ...

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete an object. Idempotent — does not raise if key missing."""
        ...

    @abstractmethod
    async def list(self, prefix: str, limit: int = 100) -> list[StorageObject]:
        """List objects with the given prefix."""
        ...

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if an object exists."""
        ...

    @abstractmethod
    async def get_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        """Generate a pre-signed URL for direct client access."""
        ...

    @abstractmethod
    async def copy(self, source_key: str, dest_key: str) -> StorageObject:
        """Copy an object within the same storage backend."""
        ...
