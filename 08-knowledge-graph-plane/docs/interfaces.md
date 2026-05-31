# Knowledge Graph Plane — Interface Contracts

## GraphStoreInterface

**Location:** `src/knowledge_graph/interfaces/graph_store.py`

```python
class GraphStoreInterface(PluginBase, ABC):
    """
    Vendor-neutral property graph storage interface.
    Implementations: KuzuAdapter, Neo4jAdapter
    Plugin group: kop.graph_adapters
    """

    @abstractmethod
    async def create_node(
        self,
        tenant_id: UUID,
        node_type: str,
        properties: dict,
        node_id: UUID | None = None,
    ) -> GraphNode:
        """Create a node in the graph. node_type must match a registered OWL class."""
        ...

    @abstractmethod
    async def get_node(self, tenant_id: UUID, node_id: UUID) -> GraphNode: ...

    @abstractmethod
    async def update_node(
        self, tenant_id: UUID, node_id: UUID, properties: dict
    ) -> GraphNode: ...

    @abstractmethod
    async def delete_node(self, tenant_id: UUID, node_id: UUID) -> None:
        """Delete a node and all its relationships."""
        ...

    @abstractmethod
    async def create_relationship(
        self,
        tenant_id: UUID,
        rel_type: str,
        from_node_id: UUID,
        to_node_id: UUID,
        properties: dict | None = None,
        valid_from: datetime | None = None,
        valid_to: datetime | None = None,
    ) -> GraphRelationship: ...

    @abstractmethod
    async def get_relationships(
        self,
        tenant_id: UUID,
        node_id: UUID,
        rel_type: str | None = None,
        direction: RelationshipDirection = RelationshipDirection.BOTH,
    ) -> list[GraphRelationship]: ...

    @abstractmethod
    async def query(
        self,
        tenant_id: UUID,
        cypher: str,
        parameters: dict | None = None,
    ) -> list[dict]:
        """
        Execute a Cypher query scoped to the tenant's graph.
        Cypher is the common query language for both Kuzu and Neo4j.
        """
        ...

    @abstractmethod
    async def get_subgraph(
        self,
        tenant_id: UUID,
        root_node_id: UUID,
        depth: int = 2,
        rel_types: list[str] | None = None,
    ) -> GraphSubgraph: ...

    @abstractmethod
    async def find_path(
        self,
        tenant_id: UUID,
        from_node_id: UUID,
        to_node_id: UUID,
        max_hops: int = 5,
    ) -> list[GraphPath]: ...
```

---

## GraphSchemaInterface

**Location:** `src/knowledge_graph/interfaces/schema.py`

```python
class GraphSchemaInterface(ABC):
    """
    Manages the graph schema — node types and relationship types.
    Schema is derived from registered ontologies.
    """

    @abstractmethod
    async def register_node_type(
        self, node_type: NodeTypeDefinition, tenant_id: UUID
    ) -> None: ...

    @abstractmethod
    async def register_relationship_type(
        self, rel_type: RelationshipTypeDefinition, tenant_id: UUID
    ) -> None: ...

    @abstractmethod
    async def validate_node(
        self, node_type: str, properties: dict, tenant_id: UUID
    ) -> SchemaValidationResult: ...
```

---

## Key Models

```python
class GraphNode(TenantScopedModel):
    node_type: str
    properties: dict
    canonical_entity_id: UUID | None = None
    labels: list[str] = []

class GraphRelationship(TenantScopedModel):
    relationship_type: str
    from_node_id: UUID
    to_node_id: UUID
    properties: dict = {}
    valid_from: datetime | None = None
    valid_to: datetime | None = None

class GraphSubgraph(BaseModel):
    nodes: list[GraphNode]
    relationships: list[GraphRelationship]
    tenant_id: UUID

class RelationshipDirection(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"
    BOTH = "both"
```
