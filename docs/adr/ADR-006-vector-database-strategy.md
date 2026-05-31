# ADR-006: Vector Database — Qdrant Primary with Adapter Pattern

## Status
Accepted

## Date
2025-05-31

## Context

The platform requires vector storage for:
- Semantic search (document embeddings)
- Entity embeddings (knowledge graph nodes)
- Ontology concept embeddings
- RAG pipeline retrieval
- Similarity-based entity resolution

Evaluated candidates:
- **Qdrant**: Open-source, Rust-based, high performance, rich filtering, sparse vector support
- **Chroma**: Open-source, Python-native, lightweight, development-friendly
- **Pinecone**: Managed, high performance, proprietary (violates Open Source First)
- **Milvus**: Open-source, distributed, complex operational setup
- **pgvector**: PostgreSQL extension — sufficient for small scale, not for production vector search
- **Weaviate**: Open-source, vector + graph hybrid, complex multi-tenancy

## Decision

**Qdrant** is the primary vector backend. **Chroma**, **Pinecone**, and **Milvus** are available as adapters.

**Rationale:**
1. Qdrant supports **sparse + dense vectors** natively — enabling true hybrid search (BM25 + semantic)
2. Strong **payload filtering** on metadata (tenant_id, domain, classification)
3. **Tenant isolation** via collection namespacing or Qdrant's native multi-tenancy
4. Best-in-class performance benchmarks for high-dimensional vectors
5. Fully open-source (Apache 2.0)
6. Active development with a production-ready REST + gRPC API

### Embedding Registry
A key platform decision: embeddings are not just stored — they are **registered** with:
- The model that produced them (e.g., `text-embedding-3-large`, `nomic-embed-text`)
- The model version
- The embedding strategy (full-document, chunk, entity, concept)
- The timestamp

This enables re-embedding when models are upgraded without losing historical embeddings.

See [ADR-018](ADR-018-embedding-registry.md) for the embedding registry strategy.

### Collection Naming Convention
```
{tenant_id}_{domain}_{embedding_type}_{model_version}
Example: acme_corp_banking_document_text3large_v2
```

## Consequences

### Positive
- Sparse + dense hybrid search in a single backend
- Strong metadata filtering for governed retrieval
- Active OSS community
- Horizontal scaling via distributed mode

### Negative
- Qdrant requires separate infrastructure (not embedded like Kuzu)
- Collection management complexity increases with multi-tenancy at scale
- Qdrant's distributed mode requires additional operational knowledge

### Neutral
- Chroma adapter covers lightweight development scenarios
- Pinecone adapter covers managed-cloud preference scenarios

## Alternatives Considered

### Alternative 1: pgvector as Primary
**Why rejected:** PostgreSQL-level vector search does not scale to billions of vectors. Lacks ANN indexing performance of dedicated vector databases.

### Alternative 2: Weaviate as Primary
**Why rejected:** Weaviate's multi-tenancy and hybrid search are strong, but its operational complexity and resource footprint exceed Qdrant for the platform's primary use case.

### Alternative 3: Pinecone as Primary
**Why rejected:** Proprietary. Violates Open Source First principle. Monthly cost at scale is prohibitive for OSS users.

## References
- [ADR-018](ADR-018-embedding-registry.md) — Embedding Registry design
- [Vector Plane](../../09-vector-plane/)
- [ADR-007](ADR-007-search-architecture.md) — Hybrid search uses vector plane
