# Ingestion Plane — Interface Contracts

## ConnectorInterface

**Location:** `src/ingestion/interfaces/connector.py`

```python
class ConnectorInterface(PluginBase, ABC):
    """
    Base interface for all ingestion source connectors.
    Every connector is a plugin registered under kop.connectors.
    """

    @abstractmethod
    async def test_connection(self) -> ConnectionStatus:
        """Test connectivity to the source system. Called at registration."""
        ...

    @abstractmethod
    async def list_assets(
        self,
        path: str | None = None,
        filters: IngestionFilters | None = None,
    ) -> AsyncIterator[AssetDescriptor]:
        """
        Stream descriptors of available assets from the source.
        Does not download content — only lists what is available.
        """
        ...

    @abstractmethod
    async def fetch_asset(self, descriptor: AssetDescriptor) -> RawAsset:
        """
        Fetch the content and metadata for a single asset.
        Returns raw bytes + source metadata.
        """
        ...

    @abstractmethod
    async def get_schema(self) -> ConnectorSchema:
        """
        Return the schema of this connector's configuration.
        Used by the Control Plane to render configuration UIs.
        """
        ...
```

---

## IngestionPipelineInterface

**Location:** `src/ingestion/interfaces/pipeline.py`

```python
class IngestionPipelineInterface(ABC):
    """
    Orchestrates the flow: fetch → parse → classify → store → emit event.
    """

    @abstractmethod
    async def run(
        self,
        connector: ConnectorInterface,
        config: IngestionConfig,
        tenant_id: UUID,
    ) -> IngestionResult:
        """Execute the full ingestion pipeline for a connector."""
        ...

    @abstractmethod
    async def run_single(
        self,
        descriptor: AssetDescriptor,
        connector: ConnectorInterface,
        tenant_id: UUID,
    ) -> AssetIngestionResult:
        """Ingest a single asset descriptor."""
        ...
```

---

## ConnectorRegistry

**Location:** `src/ingestion/registry/connector_registry.py`

```python
class ConnectorRegistry:
    """
    Manages registered connector plugins.
    Connectors are discovered at startup and retrievable by ID.
    """

    def register(self, connector_class: type[ConnectorInterface]) -> None: ...
    def get(self, connector_id: str) -> type[ConnectorInterface]: ...
    def list_registered(self) -> list[ConnectorInfo]: ...
    def get_schema(self, connector_id: str) -> ConnectorSchema: ...
```

---

## Key Models

```python
class AssetDescriptor(BaseModel):
    """A lightweight reference to an asset in a source system."""
    source_uri: str
    connector_id: str
    content_type: str | None
    size_bytes: int | None
    last_modified: datetime | None
    source_metadata: dict

class RawAsset(BaseModel):
    descriptor: AssetDescriptor
    content: bytes
    detected_content_type: str
    source_metadata: dict

class IngestionResult(BaseModel):
    job_id: UUID
    tenant_id: UUID
    connector_id: str
    total_assets: int
    succeeded: int
    failed: int
    errors: list[IngestionError]
    duration_seconds: float
```
