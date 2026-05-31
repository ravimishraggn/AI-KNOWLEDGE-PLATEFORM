# Architecture Decision Records (ADRs)

Architecture Decision Records document significant technical decisions made during the design and evolution of the Knowledge Operating Platform.

## Format

Each ADR follows the [MADR format](https://adr.github.io/madr/):

```
# ADR-NNN: Title

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-NNN]

## Context
Why does this decision need to be made? What is the problem or constraint?

## Decision
What was decided?

## Consequences
What becomes easier? What becomes harder? What are the trade-offs?

## Alternatives Considered
What else was evaluated and why was it rejected?
```

---

## ADR Index

| ADR | Title | Status | Plane(s) |
|-----|-------|--------|----------|
| [ADR-001](ADR-001-api-first-architecture.md) | API-First Architecture | Accepted | All |
| [ADR-002](ADR-002-event-driven-architecture.md) | Event-Driven Architecture with Redis Streams | Accepted | All |
| [ADR-003](ADR-003-multi-tenant-strategy.md) | Multi-Tenant Strategy — Schema-per-Tenant | Accepted | All |
| [ADR-004](ADR-004-plugin-architecture.md) | Plugin Architecture via Entry Points | Accepted | All |
| [ADR-005](ADR-005-knowledge-graph-selection.md) | Knowledge Graph — Kuzu Primary, Neo4j Adapter | Accepted | 08-knowledge-graph |
| [ADR-006](ADR-006-vector-database-strategy.md) | Vector Database — Qdrant Primary with Adapter Pattern | Accepted | 09-vector |
| [ADR-007](ADR-007-search-architecture.md) | Search Architecture — Hybrid Search via OpenSearch | Accepted | 10-search |
| [ADR-008](ADR-008-ontology-management.md) | Ontology Management — OWL/SKOS with Custom Registry | Accepted | 05-ontology |
| [ADR-009](ADR-009-metadata-strategy.md) | Metadata Strategy — Unified Technical and Business Metadata | Accepted | 03-metadata |
| [ADR-010](ADR-010-governance-model.md) | Governance Model — RBAC + ABAC with Policy Engine | Accepted | 11-governance |
| [ADR-011](ADR-011-lineage-tracking.md) | Lineage Tracking — Event-Sourced Graph | Accepted | 12-lineage |
| [ADR-012](ADR-012-semantic-layer.md) | Semantic Layer — Governed Business Glossary | Accepted | 07-semantic |
| [ADR-013](ADR-013-authentication-strategy.md) | Authentication — Pluggable with JWT Default | Accepted | 01-foundation |
| [ADR-014](ADR-014-cloud-neutral-storage.md) | Cloud-Neutral Storage Abstraction | Accepted | 01-foundation |
| [ADR-015](ADR-015-python-fastapi-choice.md) | Python + FastAPI as Primary API Framework | Accepted | All |
| [ADR-016](ADR-016-canonical-model-strategy.md) | Canonical Model Strategy — Registry-Based Entity Resolution | Accepted | 04-canonical |
| [ADR-017](ADR-017-mcp-agent-protocol.md) | Agent Protocol — MCP as Primary Agent Interface | Accepted | 15-agent |
| [ADR-018](ADR-018-embedding-registry.md) | Embedding Registry — Model-Versioned Embeddings | Accepted | 09-vector |
| [ADR-019](ADR-019-rag-architecture.md) | RAG Architecture — Modular Pipeline with Context Assembly | Accepted | 14-ai-consumption |
| [ADR-020](ADR-020-data-sovereignty.md) | Data Sovereignty — Tenant-Bound Classification and Residency | Accepted | 11-governance |

---

## Template

Use [ADR-000-template.md](ADR-000-template.md) as the starting point for new ADRs.

## Process

1. Copy the template and number it sequentially
2. Set status to `Proposed`
3. Open a PR with the ADR as the only file changed
4. Once approved, set status to `Accepted`
5. If superseded, update status and link to the new ADR
