# Metadata Plane — Interface Contracts

## MetadataHarvesterInterface

**Location:** `src/metadata/interfaces/harvester.py`

```python
class MetadataHarvesterInterface(PluginBase, ABC):
    """
    Extracts technical metadata from a specific asset type.
    Implementations: DocumentHarvester, DatabaseTableHarvester, APIEndpointHarvester
    """

    @abstractmethod
    async def can_handle(self, asset_type: str, content_type: str) -> bool:
        """Return True if this harvester handles the given asset/content type."""
        ...

    @abstractmethod
    async def harvest(self, asset: RawAsset, tenant_id: UUID) -> TechnicalMetadata:
        """
        Extract technical metadata from the asset.
        Must not modify the asset content.
        """
        ...
```

---

## MetadataCatalogInterface

**Location:** `src/metadata/interfaces/catalog.py`

```python
class MetadataCatalogInterface(ABC):
    """
    The primary catalog API — CRUD for asset metadata records.
    """

    @abstractmethod
    async def register_asset(self, metadata: AssetMetadata) -> AssetMetadata: ...

    @abstractmethod
    async def get_asset(self, asset_id: UUID, tenant_id: UUID) -> AssetMetadata: ...

    @abstractmethod
    async def update_business_metadata(
        self, asset_id: UUID, tenant_id: UUID, updates: BusinessMetadataUpdate
    ) -> AssetMetadata: ...

    @abstractmethod
    async def search_catalog(
        self, query: CatalogQuery, tenant_id: UUID
    ) -> PaginatedResponse[AssetMetadata]: ...

    @abstractmethod
    async def get_quality_score(self, asset_id: UUID, tenant_id: UUID) -> QualityScore: ...

    @abstractmethod
    async def delete_asset(self, asset_id: UUID, tenant_id: UUID) -> None: ...
```

---

## Key Models

```python
class AssetMetadata(TenantScopedModel):
    asset_type: AssetType
    source_system: str
    source_uri: str
    storage_key: str
    technical: TechnicalMetadata
    business: BusinessMetadata
    governance: GovernanceMetadata
    quality_score: float | None = None
    version: int = 1

class TechnicalMetadata(BaseModel):
    content_type: str
    size_bytes: int
    format: str | None
    schema_info: dict | None
    language: str | None
    encoding: str | None
    hash_sha256: str

class BusinessMetadata(BaseModel):
    name: str | None = None
    description: str | None = None
    owner: str | None = None
    steward: str | None = None
    domain: str | None = None
    tags: list[str] = []
    glossary_terms: list[UUID] = []

class GovernanceMetadata(BaseModel):
    classification: DataClassification = DataClassification.UNCLASSIFIED
    policy_ids: list[UUID] = []
    sovereignty_zone: str | None = None
    retention_days: int | None = None
```
