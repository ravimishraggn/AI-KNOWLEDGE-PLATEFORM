# ADR-011: Lineage Tracking — Event-Sourced Graph

## Status
Accepted

## Date
2025-05-31

## Context

Enterprise knowledge platforms must answer:
- Where did this knowledge asset come from?
- What transformations were applied?
- Which downstream assets depend on this asset?
- If this source changes, what is the impact?
- Who approved this transformation?

Lineage must span: raw data → ingestion → metadata enrichment → canonical model → ontology concept → knowledge graph node → vector embedding → AI response.

## Decision

Lineage is tracked as an **event-sourced directed acyclic graph (DAG)**:

1. Every transformation emits a **LineageEvent** (via the event bus, ADR-002)
2. LineageEvents are consumed by the Lineage Plane and persisted as nodes/edges in a **lineage graph** (separate from the knowledge graph)
3. The lineage graph is stored in **PostgreSQL** (for small-medium scale) with a Kuzu adapter for large-scale traversal
4. Lineage is **immutable** — events are never deleted (append-only)
5. **Impact analysis** queries traverse the lineage graph downstream
6. **Provenance queries** traverse upstream

### LineageEvent Schema
```
LineageEvent:
  - event_id: UUID
  - tenant_id: UUID
  - event_type: [created | transformed | derived | classified | embedded | retrieved | consumed]
  - source_asset: AssetRef
  - target_asset: AssetRef
  - transformation: TransformationSpec
  - actor: ActorRef (user | system | agent)
  - timestamp: datetime
  - metadata: dict
```

### OpenLineage Compatibility
The Lineage Plane will adopt the **OpenLineage** standard for interoperability with data catalog tools (Marquez, OpenMetadata, DataHub).

## Consequences

### Positive
- Complete end-to-end provenance for every knowledge asset
- Impact analysis enables change management
- Event sourcing enables lineage replay and audit
- OpenLineage compatibility enables integration with existing data governance tools

### Negative
- Lineage graph grows continuously — storage management required
- High-cardinality lineage traversal (deep dependency graphs) can be slow
- Requires every plane to emit lineage events (governance overhead)

## Alternatives Considered

### Alternative 1: Database Foreign Keys for Lineage
**Why rejected:** Cannot represent complex transformation graphs. Cannot record transformation metadata. No audit trail.

## References
- [ADR-002](ADR-002-event-driven-architecture.md) — Events are the lineage input
- [Lineage Plane](../../12-lineage-plane/)
