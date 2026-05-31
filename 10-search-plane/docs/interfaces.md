# Search Plane — Interface Contracts

## SearchEngineInterface

**Location:** `src/search/interfaces/engine.py`

```python
class SearchEngineInterface(PluginBase, ABC):
    """
    A single search modality engine.
    Plugin group: kop.search_engines
    """

    @property
    @abstractmethod
    def engine_id(self) -> str: ...

    @abstractmethod
    async def index(
        self,
        tenant_id: UUID,
        document: SearchDocument,
    ) -> None:
        """Index a document for search. Idempotent on document_id."""
        ...

    @abstractmethod
    async def delete(self, tenant_id: UUID, document_id: UUID) -> None:
        """Remove a document from the index."""
        ...

    @abstractmethod
    async def search(
        self,
        tenant_id: UUID,
        query: SearchQuery,
    ) -> SearchResult:
        """Execute a search and return ranked results."""
        ...

    @abstractmethod
    async def bulk_index(
        self,
        tenant_id: UUID,
        documents: list[SearchDocument],
    ) -> BulkIndexResult: ...
```

---

## UnifiedSearchInterface

**Location:** `src/search/interfaces/unified_search.py`

```python
class UnifiedSearchInterface(ABC):
    """
    The primary search API — routes, fuses, and governs search results.
    """

    @abstractmethod
    async def search(
        self,
        query: UnifiedSearchRequest,
        tenant_id: UUID,
        principal: Principal,
    ) -> UnifiedSearchResponse:
        """
        Execute search across all requested strategies.
        Apply governance filter. Fuse results. Return ranked list.
        """
        ...

    @abstractmethod
    async def suggest(
        self,
        prefix: str,
        tenant_id: UUID,
        principal: Principal,
        limit: int = 10,
    ) -> list[SearchSuggestion]:
        """Autocomplete suggestions based on prefix."""
        ...

    @abstractmethod
    async def explain(
        self,
        query: UnifiedSearchRequest,
        document_id: UUID,
        tenant_id: UUID,
    ) -> SearchExplanation:
        """Explain why a document ranked at its position."""
        ...
```

---

## Key Models

```python
class UnifiedSearchRequest(BaseModel):
    query: str
    strategies: list[str] = ["hybrid"]
    filters: dict = {}
    domains: list[str] = []
    classifications: list[DataClassification] = []
    limit: int = 20
    offset: int = 0
    include_facets: bool = False
    explain: bool = False

class UnifiedSearchResponse(BaseModel):
    query: str
    results: list[SearchHit]
    total: int
    facets: dict | None = None
    strategies_used: list[str]
    fusion_method: str
    latency_ms: float
    request_id: UUID

class SearchHit(BaseModel):
    document_id: UUID
    asset_id: UUID
    score: float
    title: str | None
    excerpt: str | None
    metadata: dict
    strategy_scores: dict[str, float]  # Per-strategy score breakdown
    explanation: SearchExplanation | None = None
```
