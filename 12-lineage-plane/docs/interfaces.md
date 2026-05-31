# Lineage Plane — Interface Contracts

## LineageTrackerInterface

**Location:** `src/lineage/interfaces/tracker.py`

```python
class LineageTrackerInterface(ABC):
    """
    Records and queries the lineage graph.
    """

    @abstractmethod
    async def record(
        self,
        event: LineageEvent,
        tenant_id: UUID,
    ) -> LineageRecord:
        """
        Record a lineage relationship. Immutable — cannot be deleted.
        Called by all planes when they transform or consume an asset.
        """
        ...

    @abstractmethod
    async def get_upstream(
        self,
        asset_id: UUID,
        tenant_id: UUID,
        depth: int = -1,
    ) -> LineageGraph:
        """
        Return all ancestors of an asset.
        depth=-1 means unlimited depth.
        """
        ...

    @abstractmethod
    async def get_downstream(
        self,
        asset_id: UUID,
        tenant_id: UUID,
        depth: int = -1,
    ) -> LineageGraph:
        """Return all descendants of an asset (impact analysis)."""
        ...

    @abstractmethod
    async def get_lineage_graph(
        self,
        asset_id: UUID,
        tenant_id: UUID,
        upstream_depth: int = 3,
        downstream_depth: int = 3,
    ) -> LineageGraph:
        """Return a combined upstream + downstream lineage graph."""
        ...

    @abstractmethod
    async def get_audit_trail(
        self,
        asset_id: UUID,
        tenant_id: UUID,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[LineageRecord]:
        """Return the chronological audit trail for an asset."""
        ...

    @abstractmethod
    async def impact_analysis(
        self,
        asset_id: UUID,
        tenant_id: UUID,
        change_type: str,
    ) -> ImpactReport:
        """Analyze the downstream impact of a change to an asset."""
        ...
```

---

## Key Models

```python
class LineageEvent(BaseModel):
    """Input to the lineage tracker — emitted by all planes."""
    tenant_id: UUID
    event_type: LineageEventType
    source_asset: AssetRef
    target_asset: AssetRef | None = None
    transformation: TransformationSpec | None = None
    actor: ActorRef
    timestamp: datetime = Field(default_factory=utcnow)
    metadata: dict = {}

class LineageRecord(TenantScopedModel):
    """Immutable record stored in the lineage graph."""
    event_type: LineageEventType
    source_asset_id: UUID
    target_asset_id: UUID | None
    transformation_type: str | None
    actor_id: str
    actor_type: str  # user | system | agent
    platform_version: str

class LineageGraph(BaseModel):
    nodes: list[LineageNode]
    edges: list[LineageEdge]
    tenant_id: UUID

class LineageEventType(str, Enum):
    CREATED = "created"
    TRANSFORMED = "transformed"
    DERIVED = "derived"
    CLASSIFIED = "classified"
    EMBEDDED = "embedded"
    RETRIEVED = "retrieved"
    CONSUMED = "consumed"
    DELETED = "deleted"

class ImpactReport(BaseModel):
    source_asset_id: UUID
    change_type: str
    affected_assets: list[AssetRef]
    affected_planes: list[str]
    risk_level: str  # low | medium | high | critical
    recommendations: list[str]
```
