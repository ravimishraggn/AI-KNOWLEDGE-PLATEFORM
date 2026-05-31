# Technology Stack — Knowledge Operating Platform

## Stack Philosophy

The technology stack is chosen to maximize: **operational reliability**, **developer productivity**, **vendor neutrality**, and **open-source alignment**.

Every technology decision is an ADR. This document summarizes the outcomes.

---

## Core Stack

### API Framework — FastAPI (Python 3.11+)

| Property | Value |
|----------|-------|
| Language | Python 3.11+ |
| Framework | FastAPI 0.110+ |
| Server | Uvicorn / Gunicorn |
| Validation | Pydantic v2 |
| Docs | OpenAPI 3.1 (auto-generated) |

**Why FastAPI:**
- Native async support for high-throughput I/O workloads
- Pydantic v2 for schema-validated contracts at every layer
- Auto-generated OpenAPI docs satisfy API-First principle
- Largest Python API ecosystem for ML/AI integration
- See [ADR-015](../adr/ADR-015-python-fastapi-choice.md)

### Relational Store — PostgreSQL 16+

| Property | Value |
|----------|-------|
| Version | PostgreSQL 16+ |
| Driver | asyncpg (async) |
| ORM | SQLAlchemy 2.0 (async) |
| Migrations | Alembic |

**Why PostgreSQL:**
- Best-in-class JSONB support for semi-structured metadata
- Row-level security for tenant isolation
- pgvector extension for lightweight vector operations
- Proven at enterprise scale

### Cache & Event Bus — Redis 7+

| Property | Value |
|----------|-------|
| Version | Redis 7+ |
| Client | redis-py (async) |
| Patterns | Cache, Pub/Sub, Redis Streams |

**Why Redis:**
- Redis Streams as lightweight event bus (Kafka adapter for high-volume)
- Session management and distributed locking
- API response caching for search and metadata endpoints

### Search Engine — OpenSearch 2+

| Property | Value |
|----------|-------|
| Version | OpenSearch 2.12+ |
| Client | opensearch-py |
| Features | BM25, semantic (kNN), hybrid, faceted |

**Why OpenSearch:**
- Fully open-source alternative to Elasticsearch
- Native kNN vector search (semantic hybrid search)
- Rich metadata filtering and aggregations
- AWS OpenSearch Service compatibility

### Graph Database — Kuzu (primary)

| Property | Value |
|----------|-------|
| Type | Embedded property graph |
| Query Language | Cypher |
| Client | kuzu Python library |

**Why Kuzu:**
- Embedded — no separate server for development and edge deployments
- Cypher query language — compatible with Neo4j skill sets
- High-performance analytical graph queries
- See [ADR-005](../adr/ADR-005-knowledge-graph-selection.md)

**Neo4j Adapter:** For organizations requiring distributed graph or existing Neo4j deployments.

### Vector Database — Qdrant (primary)

| Property | Value |
|----------|-------|
| Version | Qdrant v1.9+ |
| Client | qdrant-client (async) |
| Features | Collections, payloads, filtering, sparse vectors |

**Why Qdrant:**
- Native support for dense + sparse (hybrid) vectors
- Strong filtering on payload metadata
- REST + gRPC API, active open-source community
- See [ADR-006](../adr/ADR-006-vector-database-strategy.md)

**Adapters:** Chroma (lightweight local), Pinecone (managed), Milvus (self-hosted scale)

---

## Infrastructure Stack

### Containerization

| Tool | Purpose |
|------|---------|
| Docker | Container runtime |
| Docker Compose | Local development orchestration |
| Helm | Kubernetes deployment charts |
| Kubernetes | Production orchestration |

### Cloud (Primary: AWS)

| Service | KOP Usage |
|---------|-----------|
| S3 | Document storage, raw ingestion |
| RDS | Managed PostgreSQL |
| ElastiCache | Managed Redis |
| OpenSearch Service | Managed search |
| EKS | Kubernetes runtime |
| Bedrock | Optional LLM adapter |
| IAM | Authentication adapter |

**Adapters:** Azure (Blob, Cognitive Search, AKS), GCP (GCS, Vertex AI, GKE)

---

## Development Stack

| Tool | Purpose |
|------|---------|
| ruff | Linting + formatting |
| mypy | Static type checking |
| pytest + pytest-asyncio | Testing |
| pre-commit | Git hooks |
| pytest-cov | Coverage |
| httpx | Async test client |

---

## Observability Stack

| Tool | Purpose |
|------|---------|
| OpenTelemetry | Distributed tracing (vendor neutral) |
| Prometheus | Metrics collection |
| Grafana | Metrics visualization |
| Loki | Log aggregation |
| Jaeger | Trace visualization |

---

## Optional / Adapter Stack

| Technology | Role |
|-----------|------|
| Apache Kafka | High-volume event bus (adapter) |
| Pinecone | Vector store adapter |
| Milvus | Vector store adapter |
| Neo4j | Graph adapter |
| Weaviate | Vector + graph adapter (future) |
| Anthropic Claude | LLM adapter (AI consumption) |
| OpenAI GPT | LLM adapter (AI consumption) |
| Hugging Face | Embedding model adapter |

---

## Technology Governance

Technology additions to the core stack require:
1. An ADR documenting the rationale and alternatives considered
2. A reference implementation (not just configuration)
3. Integration tests with the relevant plane
4. Documentation in this file

Technology removals from the core stack require:
1. A deprecation notice in the relevant ADR
2. A migration path documented in the plane's future-evolution.md
3. Minimum one major version deprecation window
