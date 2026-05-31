# ADR-007: Search Architecture — Unified Hybrid Search

## Status
Accepted

## Date
2025-05-31

## Context

Enterprise knowledge search requires multiple search modalities:
- **Keyword search**: Exact term matching, BM25 ranking (lawyers, compliance use cases)
- **Semantic search**: Embedding-based similarity (conceptual queries, RAG retrieval)
- **Hybrid search**: Combine keyword + semantic for best recall/precision
- **Graph search**: Traverse relationship networks (entity discovery, impact analysis)
- **Metadata search**: Filter by classification, owner, domain, governance attributes
- **Federated search**: Query across multiple source systems simultaneously

The challenge: these are served by different backends (OpenSearch, Qdrant, Kuzu, PostgreSQL), and consumers want a single API.

## Decision

The Search Plane provides a **unified search API** that routes, merges, and ranks results from multiple backends:

1. **Single search endpoint**: `POST /v1/search` accepts a query and a list of search strategies
2. **Strategy routing**: The search router dispatches to the appropriate backend engine
3. **Result fusion**: Reciprocal Rank Fusion (RRF) merges results from multiple strategies
4. **Governance filter**: All results pass through the governance filter before being returned
5. **Tenant isolation**: Search is always scoped to the requesting tenant

### Search Architecture Layers
```
Consumer → Search API → Query Analyzer → Strategy Router
                                            ├── Keyword Engine (OpenSearch)
                                            ├── Semantic Engine (Qdrant)
                                            ├── Hybrid Engine (OpenSearch kNN + Qdrant)
                                            ├── Graph Engine (Kuzu)
                                            └── Metadata Engine (PostgreSQL)
                       ← Result Fusion (RRF) ←
                       ← Governance Filter ←
                       ← Ranking & Explanation ←
```

### OpenSearch as the Keyword and Hybrid Backbone
OpenSearch provides: BM25 keyword search, kNN vector search (OpenSearch 2.x neural plugin), faceted filtering, and aggregations. It serves as the primary search index.

Qdrant handles high-dimensional dense vector search with complex payload filtering.

## Consequences

### Positive
- Single API for all search modalities
- Consumers don't need to know which backend holds which data
- RRF fusion improves result quality vs any single modality
- Governance is enforced at the search layer — not the data layer

### Negative
- Cross-backend result fusion adds latency (~20-100ms overhead)
- Maintaining sync between OpenSearch index and source data requires careful indexing pipeline
- Complex ranking logic is harder to debug and explain

### Neutral
- Federated search adds external call latency — use timeout/circuit breaker pattern

## Alternatives Considered

### Alternative 1: Search Delegated to Each Plane
**Why rejected:** Consumers would need to call multiple APIs. No unified ranking. Governance applied inconsistently.

### Alternative 2: Elasticsearch Instead of OpenSearch
**Why rejected:** OpenSearch is fully open-source. Elasticsearch licensing changed (SSPL) in 2021. OpenSearch is the OSS community fork.

## References
- [ADR-006](ADR-006-vector-database-strategy.md) — Vector backend used by semantic search
- [Search Plane](../../10-search-plane/)
