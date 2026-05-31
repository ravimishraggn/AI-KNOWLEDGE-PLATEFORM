# 09 — Vector Plane

The Vector Plane manages **semantic embeddings** for all knowledge assets. It provides multi-backend vector storage, an embedding registry for model governance, and high-performance similarity search.

---

## Responsibilities

- Embed knowledge assets using registered embedding models
- Store embeddings in vector database backends (Qdrant primary)
- Maintain the Embedding Registry (model × version × asset tracking)
- Provide similarity search with metadata filtering
- Support sparse + dense hybrid retrieval
- Enable re-embedding workflows when models are upgraded

---

## Supported Backends

| Backend | Type | Status |
|---------|------|--------|
| **Qdrant** | Distributed vector DB (primary) | Planned |
| **Chroma** | Embedded vector DB (dev/lightweight) | Planned |
| **Pinecone** | Managed cloud vector DB (adapter) | Planned |
| **Milvus** | Self-hosted distributed vector DB (adapter) | Planned |

---

## Supported Embedding Models

| Provider | Models |
|----------|--------|
| OpenAI | text-embedding-3-large, text-embedding-3-small |
| Cohere | embed-english-v3.0, embed-multilingual-v3.0 |
| Hugging Face | nomic-embed-text, BAAI/bge-large-en |
| Anthropic | (future) |
| Local | Sentence Transformers (any HF model) |

---

## Embedding Registry

Every embedding is registered with:
- The **model** that produced it (name, version, provider, dimensions)
- The **strategy** (full-document, chunk, entity, concept)
- The **asset** it represents
- The **timestamp** it was created

This enables: model versioning, re-embedding workflows, and AI response auditing.

---

## Collection Naming

```
{tenant_id}_{domain}_{embedding_type}_{model_key}
Example: tenant_acme_banking_document_text3large
```

---

## Events Consumed

- `kop.metadata.asset.harvested.v1` → triggers embedding pipeline

## Events Emitted

- `kop.vector.embedding.created.v1`
- `kop.vector.model.registered.v1`

---

## Plane Dependencies

- **01-foundation**: auth, event bus
- Consumed by: 10-search (semantic search), 14-ai-consumption (RAG retrieval)
