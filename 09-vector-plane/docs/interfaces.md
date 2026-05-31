# Vector Plane — Interface Contracts

## VectorStoreInterface

**Location:** `src/vector/interfaces/store.py`

```python
class VectorStoreInterface(PluginBase, ABC):
    """
    Vendor-neutral vector storage interface.
    Implementations: QdrantAdapter, ChromaAdapter, PineconeAdapter, MilvusAdapter
    Plugin group: kop.vector_adapters
    """

    @abstractmethod
    async def upsert(
        self,
        tenant_id: UUID,
        collection_name: str,
        vectors: list[VectorRecord],
    ) -> UpsertResult:
        """Upsert vectors into a collection. Creates collection if not exists."""
        ...

    @abstractmethod
    async def search(
        self,
        tenant_id: UUID,
        collection_name: str,
        query_vector: list[float],
        limit: int = 10,
        filters: VectorFilter | None = None,
        with_payload: bool = True,
    ) -> list[ScoredVector]:
        """Dense vector similarity search with optional payload filtering."""
        ...

    @abstractmethod
    async def hybrid_search(
        self,
        tenant_id: UUID,
        collection_name: str,
        query_vector: list[float],
        sparse_vector: dict[int, float],
        limit: int = 10,
        filters: VectorFilter | None = None,
    ) -> list[ScoredVector]:
        """Combined dense + sparse (BM25) hybrid search."""
        ...

    @abstractmethod
    async def get_by_id(
        self,
        tenant_id: UUID,
        collection_name: str,
        vector_id: UUID,
    ) -> VectorRecord | None: ...

    @abstractmethod
    async def delete(
        self,
        tenant_id: UUID,
        collection_name: str,
        vector_ids: list[UUID],
    ) -> None: ...

    @abstractmethod
    async def create_collection(
        self,
        collection_name: str,
        dimensions: int,
        distance_metric: DistanceMetric = DistanceMetric.COSINE,
    ) -> None: ...

    @abstractmethod
    async def delete_collection(self, collection_name: str) -> None: ...

    @abstractmethod
    async def collection_info(self, collection_name: str) -> CollectionInfo: ...
```

---

## EmbeddingModelInterface

**Location:** `src/vector/interfaces/embedding.py`

```python
class EmbeddingModelInterface(PluginBase, ABC):
    """
    Interface for embedding model providers.
    Plugin group: kop.embedding_models
    """

    @property
    @abstractmethod
    def dimensions(self) -> int:
        """Output vector dimensions."""
        ...

    @property
    @abstractmethod
    def max_tokens(self) -> int:
        """Maximum input tokens."""
        ...

    @abstractmethod
    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts. Returns a list of float vectors."""
        ...

    @abstractmethod
    async def embed_query(self, text: str) -> list[float]:
        """Embed a single query text (may use different instruction prefix)."""
        ...
```

---

## Key Models

```python
class VectorRecord(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    vector: list[float]
    sparse_vector: dict[int, float] | None = None  # For hybrid search
    payload: dict                                   # Includes asset_id, model_id, tenant_id

class ScoredVector(BaseModel):
    id: UUID
    score: float
    payload: dict | None = None

class EmbeddingModelRecord(TenantScopedModel):
    """Registry entry for an embedding model."""
    name: str                # e.g., "text-embedding-3-large"
    version: str             # e.g., "2024-02"
    provider: str            # openai | huggingface | cohere | local
    dimensions: int
    max_tokens: int
    is_active: bool = True
    deprecated_at: datetime | None = None

class DistanceMetric(str, Enum):
    COSINE = "cosine"
    DOT = "dot"
    EUCLIDEAN = "euclidean"
```
