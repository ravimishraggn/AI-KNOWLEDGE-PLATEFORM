# 14 — AI Consumption Plane

The AI Consumption Plane transforms the Knowledge Operating Platform into the **ground truth engine for enterprise AI**. It provides RAG pipelines, context assembly APIs, and governed semantic retrieval.

---

## Responsibilities

- Provide RAG (Retrieval Augmented Generation) pipeline infrastructure
- Assemble structured, governed context for AI requests
- Support advanced RAG patterns (HyDE, Graph RAG, recursive retrieval)
- Enforce governance on all AI retrievals (no unauthorized assets in AI context)
- Log every retrieval operation for lineage and audit
- Provide semantic retrieval APIs for AI application developers
- Manage retrieval quality through reranking and result fusion

---

## RAG Pipeline Architecture

```
AI Request
    → Query Analysis (intent, entities, domain)
    → Strategy Selection (which retrieval strategies to invoke)
    → Multi-Modal Retrieval (parallel)
    │   ├── Vector Search (Qdrant)
    │   ├── Graph Search (Kuzu/Neo4j)
    │   ├── Keyword Search (OpenSearch)
    │   └── Structured Metadata (PostgreSQL)
    → Reranking (cross-encoder or rule-based)
    → Context Assembly (structured, cited)
    → Governance Filter (remove unauthorized)
    → Lineage Recording
    → Return ContextBundle
```

---

## Advanced RAG Patterns

| Pattern | Description |
|---------|-------------|
| **Basic RAG** | Query → embed → vector search → context |
| **HyDE** | Generate hypothetical document → embed → search |
| **Graph RAG** | Entity extraction → graph traversal → context |
| **Structured RAG** | Return typed entities, not just text chunks |
| **Recursive RAG** | Multi-hop retrieval via knowledge graph |
| **Governed RAG** | All retrieval access-controlled and audited |

---

## Context API

```python
# Request structured context for an AI query
POST /v1/ai/context
{
  "query": "What is Goldman Sachs' credit exposure in EU markets?",
  "strategies": ["hybrid", "graph"],
  "max_context_tokens": 8000,
  "include_citations": true,
  "domains": ["banking", "risk"]
}

# Returns structured context bundle
{
  "context_items": [...],
  "citations": [...],
  "retrieval_log": [...],
  "token_count": 4821,
  "request_id": "..."
}
```

---

## Events Emitted

- `kop.ai.retrieval.executed.v1` (feeds Lineage Plane)
- `kop.ai.context.assembled.v1`

---

## Plane Dependencies

- **09-vector**: primary retrieval backend
- **08-knowledge-graph**: graph retrieval
- **10-search**: keyword/hybrid retrieval
- **11-governance**: retrieval authorization
- **12-lineage**: retrieval logging
