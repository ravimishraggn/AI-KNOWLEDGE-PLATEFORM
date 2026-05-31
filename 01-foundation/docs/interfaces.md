# Foundation Plane — Interface Contracts

All interfaces are defined as Python Abstract Base Classes (ABCs) in `src/knowledge_platform/`. These are the **design contracts** for the platform. No implementation belongs in this document.

---

## AuthProvider Interface

**Location:** `src/knowledge_platform/auth/abstract.py`

```python
class AuthProvider(ABC):

    @abstractmethod
    async def validate_token(self, token: str) -> TokenClaims:
        """Validate a bearer token and return extracted claims.
        Raises AuthenticationError if token is invalid or expired."""

    @abstractmethod
    async def extract_tenant_id(self, claims: TokenClaims) -> UUID:
        """Extract and validate the tenant_id from token claims.
        Raises AuthenticationError if tenant claim is missing or invalid."""

    @abstractmethod
    async def extract_user_id(self, claims: TokenClaims) -> str:
        """Extract the user identifier from token claims."""

    @abstractmethod
    async def extract_roles(self, claims: TokenClaims) -> list[str]:
        """Extract the list of roles assigned to this principal."""

    @abstractmethod
    async def refresh_token(self, refresh_token: str) -> TokenPair:
        """Exchange a refresh token for a new access+refresh token pair.
        Raises AuthenticationError if refresh token is invalid."""
```

**Implementations:** `JWTAuthProvider`, `OIDCAuthProvider`, `APIKeyAuthProvider`
**Plugin group:** `kop.auth`

---

## StorageInterface

**Location:** `src/knowledge_platform/storage/abstract.py`

```python
class StorageInterface(ABC):

    @abstractmethod
    async def put(self, key: str, data: bytes, metadata: dict | None = None) -> StorageObject:
        """Upload an object to storage. Creates or overwrites."""

    @abstractmethod
    async def get(self, key: str) -> bytes:
        """Download an object by key.
        Raises ObjectNotFoundError if key does not exist."""

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete an object by key. Idempotent."""

    @abstractmethod
    async def list(self, prefix: str, limit: int = 100) -> list[StorageObject]:
        """List objects with the given prefix."""

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if an object exists."""

    @abstractmethod
    async def get_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        """Generate a pre-signed URL for direct access to the object."""

    @abstractmethod
    async def copy(self, source_key: str, dest_key: str) -> StorageObject:
        """Copy an object within the same storage backend."""
```

**Implementations:** `S3StorageAdapter`, `AzureBlobAdapter`, `GCSAdapter`, `LocalFileAdapter`
**Plugin group:** `kop.storage`

---

## EventBusInterface

**Location:** `src/knowledge_platform/events/bus.py`

```python
class EventBusInterface(ABC):

    @abstractmethod
    async def publish(self, event: PlatformEvent) -> str:
        """Publish an event to the bus. Returns the event ID."""

    @abstractmethod
    async def subscribe(
        self,
        stream: str,
        group: str,
        handler: Callable[[PlatformEvent], Awaitable[None]],
        batch_size: int = 10,
    ) -> None:
        """Subscribe to a stream with a consumer group.
        Calls handler for each event. Acks on success, dead-letters on failure."""

    @abstractmethod
    async def get_stream_info(self, stream: str) -> StreamInfo:
        """Return metadata about a stream (length, groups, lag)."""

    @abstractmethod
    async def create_consumer_group(self, stream: str, group: str) -> None:
        """Create a consumer group. Idempotent."""
```

**Implementations:** `RedisStreamsEventBus`, `KafkaEventBus`
**Plugin group:** `kop.events`

---

## PluginBase Interface

**Location:** `src/knowledge_platform/plugins/base.py`

```python
class PluginBase(ABC):

    @property
    @abstractmethod
    def plugin_id(self) -> str:
        """Unique identifier for this plugin (e.g., 's3', 'neo4j')."""

    @property
    @abstractmethod
    def plugin_version(self) -> str:
        """Semantic version of this plugin implementation."""

    @property
    @abstractmethod
    def capability_type(self) -> PluginCapabilityType:
        """The type of capability this plugin provides."""

    @abstractmethod
    async def initialize(self, config: dict) -> None:
        """Initialize the plugin with configuration.
        Raises PluginInitializationError on failure."""

    @abstractmethod
    async def health_check(self) -> PluginHealth:
        """Return the health status of this plugin."""

    @abstractmethod
    async def shutdown(self) -> None:
        """Gracefully shut down the plugin."""
```

---

## Base Domain Models

**Location:** `src/knowledge_platform/models/base.py`

```python
class TenantScopedModel(BaseModel):
    """Base for all tenant-scoped domain objects."""
    id: UUID = Field(default_factory=uuid4)
    tenant_id: UUID
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
    created_by: str | None = None

class PlatformEvent(BaseModel):
    """CloudEvents-compatible event envelope."""
    id: UUID = Field(default_factory=uuid4)
    specversion: str = "1.0"
    type: str                    # kop.{plane}.{entity}.{action}.v{n}
    source: str                  # /planes/{plane}
    subject: str                 # The affected resource URI
    tenant_id: UUID
    time: datetime = Field(default_factory=utcnow)
    data: dict                   # Event-specific payload
    datacontenttype: str = "application/json"
```

---

## Standard API Response Envelopes

**Location:** `src/knowledge_platform/models/responses.py`

```python
class SuccessResponse(BaseModel, Generic[T]):
    data: T
    request_id: str
    timestamp: datetime

class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: dict | None
    request_id: str
    timestamp: datetime

class PaginatedResponse(BaseModel, Generic[T]):
    data: list[T]
    total: int
    page: int
    page_size: int
    has_next: bool
    cursor: str | None  # For cursor-based pagination
    request_id: str
```
