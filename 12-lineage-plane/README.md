# 12 — Lineage Plane

The Lineage Plane provides **end-to-end knowledge provenance** tracking. Every transformation, enrichment, embedding, and AI response is traced from origin to consumption in an immutable, queryable lineage graph.

---

## Responsibilities

- Consume lineage events from all planes
- Build and maintain the lineage DAG (directed acyclic graph)
- Provide provenance queries (upstream tracing)
- Provide impact analysis queries (downstream tracing)
- Expose OpenLineage-compatible APIs for external catalog integration
- Store lineage history immutably (append-only)

---

## Lineage Scope

| Transformation Type | Example |
|--------------------|---------|
| **Ingestion** | Raw file → Platform asset |
| **Metadata Enrichment** | Asset → AssetMetadata |
| **Classification** | AssetMetadata → ClassifiedAsset |
| **Embedding** | Asset content → Vector embedding |
| **Canonicalization** | Multiple source entities → CanonicalEntity |
| **Graph Creation** | CanonicalEntity → Graph node |
| **Knowledge Derivation** | Graph traversal → Derived insight |
| **AI Retrieval** | Knowledge assets → RAG context |
| **AI Response** | RAG context → AI response |

---

## Query Types

| Query | Returns |
|-------|---------|
| `GET /lineage/{asset_id}/upstream` | All ancestors of an asset |
| `GET /lineage/{asset_id}/downstream` | All descendants of an asset |
| `GET /lineage/{asset_id}/graph` | Full lineage subgraph |
| `POST /lineage/impact` | Impact analysis for a change |
| `GET /lineage/{asset_id}/audit` | Who touched this asset and when |

---

## OpenLineage Compatibility

The Lineage Plane emits and accepts [OpenLineage](https://openlineage.io/) events:
- Compatible with Marquez, Apache Atlas, DataHub, OpenMetadata
- Enables lineage federation with existing data governance tools

---

## Events Consumed

- All planes' state-change events contribute lineage records

---

## Plane Dependencies

- **01-foundation**: event bus (primary input), auth
- **08-knowledge-graph**: uses the graph plane for lineage graph storage (optional)
