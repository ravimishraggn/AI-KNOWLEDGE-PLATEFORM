# ADR-018: Embedding Registry — Model-Versioned Embeddings

## Status
Accepted

## Date
2025-05-31

## Context

Embeddings in vector databases become stale when the embedding model changes. Without registry metadata:
- You don't know which model produced which vectors
- You can't safely compare vectors from different models (different embedding spaces)
- You can't systematically re-embed when a model is upgraded
- You can't audit which AI responses were grounded by which embedding model

## Decision

The Vector Plane maintains an **Embedding Registry** alongside every vector collection:

1. **EmbeddingModel**: registered model with name, version, dimensions, provider, and configuration
2. Every vector in Qdrant has a **payload field** linking back to its EmbeddingModel record
3. **Re-embedding jobs**: triggered when a new model version is registered; old embeddings are not deleted until re-embedding is verified
4. **Model compatibility matrix**: records which models' vectors can be safely compared
5. **Embedding lineage**: the embedding act is recorded as a LineageEvent

### EmbeddingModel Schema
```
EmbeddingModel:
  - model_id: UUID
  - name: str  # e.g., "text-embedding-3-large"
  - version: str  # e.g., "2024-02"
  - provider: str  # openai | anthropic | huggingface | local
  - dimensions: int  # e.g., 3072
  - max_tokens: int
  - config: dict
  - deprecated_at: datetime | None
```

## Consequences

### Positive
- Full audit trail for every vector
- Safe model upgrades with parallel old/new embeddings
- Cross-model comparison prevention at the query layer
- Regulatory traceability for AI responses

### Negative
- Registry adds overhead to embedding pipelines
- Storage cost of maintaining parallel embeddings during model migrations

## References
- [ADR-006](ADR-006-vector-database-strategy.md) — Qdrant stores embeddings
- [Vector Plane](../../09-vector-plane/)
