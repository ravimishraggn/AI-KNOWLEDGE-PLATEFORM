# 10 — Search Plane

The Search Plane provides **unified, governed, multi-modal search** across all knowledge assets. It is the primary discovery interface for humans and AI systems alike.

---

## Responsibilities

- Provide a single search API across all search modalities
- Manage OpenSearch indices for keyword and hybrid search
- Route queries to appropriate search engines based on strategy
- Fuse results from multiple backends using Reciprocal Rank Fusion (RRF)
- Enforce governance filters on all search results
- Support faceted search, filtering, aggregations, and sorting
- Enable federated search across external systems

---

## Search Modalities

| Modality | Backend | Use Case |
|----------|---------|---------|
| **Keyword** | OpenSearch (BM25) | Exact term matching, regulatory search |
| **Semantic** | Qdrant (dense vectors) | Conceptual queries, RAG retrieval |
| **Hybrid** | OpenSearch kNN + Qdrant | Best recall + precision |
| **Graph** | Kuzu / Neo4j | Entity discovery, relationship traversal |
| **Metadata** | PostgreSQL | Filter by owner, domain, classification |
| **Federated** | External APIs | Cross-system search |

---

## Unified Search API

```
POST /v1/search
{
  "query": "credit risk exposure for Goldman Sachs",
  "strategies": ["hybrid", "graph"],
  "filters": {
    "domain": "banking",
    "classification": ["INTERNAL", "CONFIDENTIAL"]
  },
  "limit": 20,
  "explain": true
}
```

---

## Result Fusion

Results from multiple strategies are merged using **Reciprocal Rank Fusion (RRF)**:
```
score(d) = Σ 1 / (k + rank_i(d))
```
where `k=60` (standard) and `rank_i` is the position in each strategy's result list.

---

## Governance Filter

All search results pass through the governance filter before being returned:
- Tenant scope enforced
- Access control checked (RBAC + ABAC)
- Classified assets filtered by clearance level
- Sovereignty zone violations rejected

---

## Events Consumed

- `kop.metadata.asset.harvested.v1` → triggers search indexing
- `kop.governance.policy.updated.v1` → triggers re-index with new access controls

---

## Plane Dependencies

- **01-foundation**: auth, event bus
- **09-vector**: semantic search queries
- **08-knowledge-graph**: graph search queries
- **11-governance**: result filtering
