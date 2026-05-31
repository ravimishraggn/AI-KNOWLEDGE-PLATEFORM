# ADR-002: Event-Driven Architecture with Redis Streams

## Status
Accepted

## Date
2025-05-31

## Context

The Knowledge Operating Platform has 20 planes, many of which need to react to state changes in other planes. Examples:
- When a document is ingested, the Metadata Plane must harvest metadata
- When an entity is created, the Knowledge Graph Plane must create a node
- When a governance policy changes, the Search Plane must re-index with new access controls
- Every transformation must emit a lineage event

Coupling these operations synchronously (REST calls) would create: tight coupling, cascading failures, and synchronous latency on write operations.

## Decision

The platform adopts **Event-Driven Architecture** with the following constraints:

1. All significant state transitions emit **CloudEvents-compatible** events
2. **Redis Streams** is the default event bus (zero additional infrastructure for small deployments)
3. **Apache Kafka** is available as an adapter for high-volume enterprise deployments
4. Event schemas are **versioned contracts** defined in `01-foundation/src/knowledge_platform/events/`
5. Events are the **primary lineage trail** — every transformation is recorded as an event
6. Consumer groups enable multiple planes to react to the same event independently

### Event Naming Convention
```
kop.{plane}.{entity}.{action}.v{version}
Examples:
  kop.ingestion.document.created.v1
  kop.metadata.asset.enriched.v1
  kop.governance.policy.updated.v1
  kop.lineage.transformation.recorded.v1
```

## Consequences

### Positive
- Loose coupling between planes — planes don't know about each other's implementation
- Events serve as the audit trail for lineage
- Planes can evolve independently without coordination
- Replay capability for disaster recovery and back-filling
- Observable by design — event stream is the single source of truth for "what happened"

### Negative
- Eventual consistency: downstream planes see changes after some delay
- Event schema evolution requires backwards compatibility discipline
- Debugging event-driven flows requires distributed tracing
- Dead-letter queue management adds operational complexity

### Neutral
- Redis Streams has a 10M event default retention — configurable per deployment
- Kafka migration path is clear when needed

## Alternatives Considered

### Alternative 1: Synchronous REST Calls Between Planes
**Why rejected:** Creates tight coupling, cascading failures, and synchronous latency. Does not support lineage replay.

### Alternative 2: Apache Kafka from Day One
**Why rejected:** Adds operational complexity (Zookeeper/KRaft, topic management) for small deployments. Redis Streams covers 90% of use cases with zero additional infrastructure.

### Alternative 3: Database Polling / Outbox Pattern Only
**Why rejected:** Polling adds latency and database load. Outbox pattern is used as a reliability mechanism for the event bus, not as a replacement.

## References
- [ADR-011](ADR-011-lineage-tracking.md) — Lineage uses events as its primary input
- [Foundation Events](../../01-foundation/src/knowledge_platform/events/)
