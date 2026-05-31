# 02 — Ingestion Plane

The Ingestion Plane is the **universal data entry point** for the Knowledge Operating Platform. Every piece of knowledge — document, record, API response, or database row — enters the platform through this plane.

---

## Responsibilities

- Connect to source systems via registered connector plugins
- Extract content with schema-aware parsing
- Apply initial data classification heuristics
- Emit `DocumentCreatedEvent` for downstream planes to consume
- Track ingestion status, retries, and failures
- Manage connector configuration and secrets

---

## Supported Connectors

| Connector | Status | Source Type |
|-----------|--------|-------------|
| S3 | Planned | Cloud Storage |
| Azure Blob | Planned | Cloud Storage |
| SharePoint | Planned | Collaboration |
| Confluence | Planned | Collaboration |
| Jira | Planned | Project Mgmt |
| GitHub | Planned | Code/Docs |
| PostgreSQL | Planned | Database |
| SQL Server | Planned | Database |
| Oracle | Planned | Database |
| MongoDB | Planned | Database |
| REST API | Planned | Web/API |
| Filesystem | Planned | Local/NFS |

---

## Architecture

```
Source System → Connector Plugin → Ingestion Pipeline → Storage → Event Bus
                                        │
                                   [Classification]
                                   [Chunking]
                                   [Metadata extraction]
```

---

## Connector Interface

All connectors implement `ConnectorInterface`. See [docs/interfaces.md](docs/interfaces.md).

New connectors are registered as plugins:
```toml
[project.entry-points."kop.connectors"]
my_connector = "my_package:MyConnector"
```

---

## Events Emitted

| Event | When |
|-------|------|
| `kop.ingestion.document.created.v1` | Successful ingestion |
| `kop.ingestion.document.failed.v1` | Ingestion failure |
| `kop.ingestion.job.started.v1` | Batch job started |
| `kop.ingestion.job.completed.v1` | Batch job completed |

---

## Key Design Decisions

- Connectors are plugins — not hardcoded in the ingestion plane
- Ingestion is idempotent: re-ingesting the same document updates, not duplicates
- Content is stored in the Storage Abstraction (S3) before metadata is extracted
- Events are emitted even on partial failure (idempotency key prevents re-processing)

---

## Plane Dependencies

- **01-foundation**: auth, storage, event bus, plugin registry
- Emits events consumed by: 03-metadata, 08-knowledge-graph, 09-vector, 12-lineage
