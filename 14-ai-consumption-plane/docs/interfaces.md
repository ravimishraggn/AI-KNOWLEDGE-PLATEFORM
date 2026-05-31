# AI Consumption Plane — Interface Contracts

## RAGPipelineInterface

**Location:** `src/ai_consumption/interfaces/rag_pipeline.py`

```python
class RAGPipelineInterface(ABC):
    """
    Modular RAG pipeline with pluggable stages.
    Each stage implements a specific interface and can be replaced.
    """

    @abstractmethod
    async def retrieve(
        self,
        query: RAGQuery,
        tenant_id: UUID,
        principal: Principal,
    ) -> RetrievalResult:
        """
        Execute the full retrieval pipeline.
        Returns governed, ranked, and cited retrieval results.
        """
        ...

    @abstractmethod
    async def assemble_context(
        self,
        retrieval_result: RetrievalResult,
        max_tokens: int,
        format: ContextFormat,
    ) -> ContextBundle:
        """
        Assemble retrieval results into structured LLM context.
        Truncates intelligently to fit max_tokens.
        """
        ...
```

---

## RetrieverInterface

**Location:** `src/ai_consumption/interfaces/retriever.py`

```python
class RetrieverInterface(PluginBase, ABC):
    """
    A single retrieval strategy. Multiple retrievers run in parallel.
    Plugin group: kop.retrievers
    """

    @property
    @abstractmethod
    def retriever_id(self) -> str: ...

    @abstractmethod
    async def retrieve(
        self,
        query: RAGQuery,
        tenant_id: UUID,
        limit: int = 20,
    ) -> list[RetrievedItem]:
        """Execute retrieval and return scored items."""
        ...
```

---

## RerankerInterface

**Location:** `src/ai_consumption/interfaces/reranker.py`

```python
class RerankerInterface(PluginBase, ABC):
    """
    Reranks multi-modal retrieval results.
    Plugin group: kop.rerankers
    """

    @abstractmethod
    async def rerank(
        self,
        query: str,
        items: list[RetrievedItem],
        top_k: int,
    ) -> list[RetrievedItem]:
        """Rerank retrieved items by relevance to the query."""
        ...
```

---

## Key Models

```python
class RAGQuery(BaseModel):
    query: str
    strategies: list[str] = ["hybrid"]
    domains: list[str] = []
    filters: dict = {}
    max_results: int = 20
    include_citations: bool = True
    rerank: bool = True

class RetrievedItem(BaseModel):
    item_id: UUID
    asset_id: UUID
    content: str
    content_type: str  # text_chunk | entity | relationship | definition
    score: float
    source: str        # retriever_id that produced this
    metadata: dict
    citation: Citation | None = None

class ContextBundle(BaseModel):
    query: str
    context_items: list[RetrievedItem]
    citations: list[Citation]
    token_count: int
    retrieval_log: list[dict]
    tenant_id: UUID
    request_id: UUID

class ContextFormat(str, Enum):
    MARKDOWN = "markdown"
    JSON = "json"
    XML = "xml"
    PLAIN_TEXT = "plain_text"
```
