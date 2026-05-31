# Platform Event Schema — v1

## Envelope

All events use the [CloudEvents 1.0](https://cloudevents.io/) envelope:

```json
{
  "specversion": "1.0",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "kop.ingestion.document.created.v1",
  "source": "/planes/ingestion",
  "subject": "/assets/550e8400-e29b-41d4-a716-446655440001",
  "time": "2025-05-31T12:00:00Z",
  "datacontenttype": "application/json",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440002",
  "data": { ... }
}
```

## Event Type Naming Convention

```
kop.{plane}.{entity}.{action}.v{version}

plane:  ingestion | metadata | ontology | canonical | taxonomy | semantic |
        knowledge_graph | vector | search | governance | lineage |
        ai | agent | analytics | control

entity: the domain entity being acted upon (snake_case)
action: the past-tense verb (created, updated, deleted, published, ...)
version: integer (start at 1, increment on breaking schema changes)
```

## Registered Events v1

| Event Type | Emitted By | Consumed By |
|-----------|-----------|------------|
| `kop.ingestion.document.created.v1` | Ingestion | Metadata, Vector, Lineage |
| `kop.ingestion.document.failed.v1` | Ingestion | Observability |
| `kop.metadata.asset.harvested.v1` | Metadata | Search (index), Vector (embed), Governance |
| `kop.metadata.asset.classified.v1` | Metadata | Governance, Lineage |
| `kop.ontology.ontology.published.v1` | Ontology | Semantic, Knowledge Graph |
| `kop.canonical.entity.created.v1` | Canonical | Knowledge Graph |
| `kop.canonical.entity.merged.v1` | Canonical | Knowledge Graph, Lineage |
| `kop.knowledge_graph.node.created.v1` | Knowledge Graph | Lineage, Search |
| `kop.knowledge_graph.relationship.created.v1` | Knowledge Graph | Lineage |
| `kop.vector.embedding.created.v1` | Vector | Lineage |
| `kop.governance.policy.updated.v1` | Governance | Search (re-filter), All planes |
| `kop.governance.access.denied.v1` | Governance | Observability, Audit |
| `kop.lineage.transformation.recorded.v1` | All planes → Lineage | Observability |
| `kop.ai.retrieval.executed.v1` | AI Consumption | Lineage, Observability |
| `kop.agent.tool.called.v1` | Agent Consumption | Lineage, Audit |
| `kop.control.tenant.provisioned.v1` | Control | All planes (setup) |

## Schema Evolution Rules

1. **v1 schemas**: backwards compatible additions only (new optional fields)
2. **Breaking change**: create `v2` event type, emit both `v1` and `v2` for one major version
3. **Retire old version**: one major platform version after `v2` is established
4. **Never change**: `id`, `type`, `source`, `subject`, `tenant_id`, `time`
