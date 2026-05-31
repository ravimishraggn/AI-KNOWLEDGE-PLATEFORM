# 08 — Knowledge Graph Plane

The Knowledge Graph Plane provides **enterprise property graph management** — the relational backbone of the knowledge platform where entities, relationships, and context are stored and traversed.

---

## Responsibilities

- Manage entity nodes (organizations, people, products, instruments, locations)
- Manage typed, directed relationships between entities
- Execute graph queries (path finding, subgraph extraction, pattern matching)
- Maintain schema consistency with the Ontology Plane
- Support temporal relationships (time-bounded edges)
- Provide graph adapters for Kuzu and Neo4j

---

## Supported Backends

| Backend | Type | Status |
|---------|------|--------|
| **Kuzu** | Embedded graph DB (primary) | Planned |
| **Neo4j** | Distributed graph DB (adapter) | Planned |

---

## Core Graph Model

```
Node (entity)
├── node_id: UUID
├── node_type: str  (matches OWL class)
├── canonical_entity_id: UUID | None
├── properties: dict
└── tenant_id: UUID

Relationship (edge)
├── relationship_id: UUID
├── relationship_type: str  (matches OWL object property)
├── from_node_id: UUID
├── to_node_id: UUID
├── properties: dict
├── valid_from: datetime | None
├── valid_to: datetime | None
└── tenant_id: UUID
```

---

## Query Capabilities

| Query Type | Example |
|-----------|---------|
| Node lookup | Find all entities of type "Organisation" |
| Relationship traversal | Get all relationships of a node |
| Path finding | Shortest path between two entities |
| Subgraph extraction | Extract 2-hop subgraph around an entity |
| Pattern matching | Find all "Person WORKS_FOR Organisation" patterns |
| Temporal query | Get relationships valid as of 2024-01-01 |

---

## Events Consumed

- `kop.metadata.asset.harvested.v1` → creates graph nodes for entities

## Events Emitted

- `kop.knowledge_graph.node.created.v1`
- `kop.knowledge_graph.relationship.created.v1`

---

## Plane Dependencies

- **01-foundation**: auth, event bus
- **05-ontology**: node type and relationship type schemas
- **04-canonical**: canonical entity resolution
- Consumed by: 10-search, 12-lineage, 14-ai-consumption, 15-agent-consumption
