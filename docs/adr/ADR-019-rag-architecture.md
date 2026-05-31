# ADR-019: RAG Architecture — Modular Pipeline with Context Assembly

## Status
Accepted

## Date
2025-05-31

## Context

RAG (Retrieval Augmented Generation) pipelines are the primary AI consumption pattern. However, naive RAG (embed query → cosine search → stuff into prompt) has well-documented failures:
- Lost-in-the-middle: relevant chunks buried in long context
- Semantic drift: retrieved chunks topically close but not factually relevant
- No governance: no record of what grounded an AI response
- No structure: unstructured text chunks vs structured knowledge entities

The platform's multi-modal knowledge store (graph, vector, metadata, ontology) enables advanced RAG patterns.

## Decision

The AI Consumption Plane implements a **modular RAG pipeline** with pluggable stages:

### Pipeline Stages
```
Query → [Query Analysis] → [Strategy Selection] → [Multi-Modal Retrieval] → [Context Assembly] → [Context Grounding] → [Response]
```

1. **Query Analysis**: intent detection, entity extraction, domain classification
2. **Strategy Selection**: determines which retrieval strategies to use
3. **Multi-Modal Retrieval**: parallel retrieval from vector, graph, metadata, and structured stores
4. **Reranking**: cross-encoder reranking of multi-modal results
5. **Context Assembly**: assembles retrieved items into structured context
6. **Context Grounding**: links context items back to their source (lineage)

### Advanced RAG Patterns Supported
- **HyDE** (Hypothetical Document Embeddings)
- **Graph RAG**: retrieve from knowledge graph + vector store jointly
- **Recursive retrieval**: multi-hop retrieval via graph traversal
- **Structured RAG**: return structured entity data, not just text chunks
- **Governed RAG**: every retrieval is access-controlled and logged

## Consequences

### Positive
- Each stage is a plugin — organizations customize the pipeline
- Every RAG response is lineage-traceable
- Multi-modal retrieval dramatically improves recall and precision
- Governed: no unauthorized assets surface in AI responses

### Negative
- Multi-stage pipeline adds latency vs simple cosine search
- More components to maintain and monitor

## References
- [AI Consumption Plane](../../14-ai-consumption-plane/)
- [ADR-007](ADR-007-search-architecture.md) — Search is a RAG retrieval backend
- [ADR-011](ADR-011-lineage-tracking.md) — RAG responses emit lineage events
