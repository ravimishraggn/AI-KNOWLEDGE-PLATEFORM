# ADR-005: Knowledge Graph — Kuzu Primary, Neo4j Adapter

## Status
Accepted

## Date
2025-05-31

## Context

The platform requires a property graph database for:
- Entity relationship modeling
- Ontology instance storage
- Knowledge graph traversal (shortest path, subgraph extraction)
- Lineage graph representation
- Temporal relationship tracking

Evaluated candidates:
- **Neo4j**: Industry leader, mature, Cypher-native, commercial licensing complexity
- **Kuzu**: Embedded, Cypher-compatible, fully open-source, analytical-grade performance
- **Apache TinkerPop / JanusGraph**: Open-source, complex operational footprint
- **Amazon Neptune**: Managed, but cloud-locked (violates Vendor Neutral principle)

## Decision

**Kuzu** is the primary graph backend. **Neo4j** is available as a first-class adapter.

**Rationale:**
1. Kuzu is **embedded** — no separate server for development or edge deployments. Dramatically lower operational overhead.
2. Kuzu uses **Cypher** — the industry standard graph query language. Neo4j developers can use the platform without re-learning.
3. Kuzu is **fully open-source** (MIT). Neo4j Community has query limitations; Neo4j Enterprise requires a commercial license.
4. Kuzu excels at **analytical graph queries** (multi-hop traversal, pattern matching) which is the platform's primary use case.
5. The **adapter pattern** (ADR-004) means Neo4j can be plugged in for organizations that require it.

### Adapter Interface
```python
# 08-knowledge-graph-plane/src/knowledge_graph/interfaces/graph_store.py
class GraphStoreInterface(ABC):
    async def create_node(self, tenant_id, node_type, properties) -> Node: ...
    async def create_relationship(self, tenant_id, rel_type, from_id, to_id, properties) -> Relationship: ...
    async def query(self, tenant_id, cypher, parameters) -> list[dict]: ...
    async def get_subgraph(self, tenant_id, node_id, depth) -> Subgraph: ...
    async def find_path(self, tenant_id, from_id, to_id, max_hops) -> list[Path]: ...
```

## Consequences

### Positive
- Zero-dependency development (Kuzu is embedded)
- Cypher compatibility with Neo4j ecosystem (tooling, training)
- Full open-source stack
- Analytical performance for knowledge graph queries

### Negative
- Kuzu is newer — smaller community than Neo4j
- Embedded Kuzu has single-writer constraint (use connection pooling)
- Distributed Kuzu not yet production-ready (as of 2025) — Neo4j adapter needed for distributed write scenarios

### Neutral
- Kuzu 1.x API is stable
- Migration from Kuzu to Neo4j via adapter requires no application code changes

## Alternatives Considered

### Alternative 1: Neo4j Community as Primary
**Why rejected:** Query limitations in Community edition. Enterprise license cost for production.

### Alternative 2: Amazon Neptune
**Why rejected:** Cloud lock-in. Violates Vendor Neutral principle (ADR-007 equivalent).

### Alternative 3: Apache TinkerPop / JanusGraph
**Why rejected:** Complex operational setup. Gremlin query language has a smaller developer community than Cypher.

## References
- [Knowledge Graph Plane](../../08-knowledge-graph-plane/)
- [ADR-004](ADR-004-plugin-architecture.md) — Adapter pattern
