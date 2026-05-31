# ADR-015: Python + FastAPI as Primary API Framework

## Status
Accepted

## Date
2025-05-31

## Context

Framework selection for the platform API layer. Requirements:
- Async-first for high-throughput I/O (database, vector search, graph queries)
- Auto-generated OpenAPI docs (API-First principle, ADR-001)
- Strong typing and schema validation
- Mature ML/AI library ecosystem
- Active open-source community
- Developer productivity

Candidates evaluated: FastAPI (Python), Django REST Framework, Flask, Go/Gin, Java/Spring Boot, Node.js/Express.

## Decision

**Python 3.11+ with FastAPI** is the primary API framework.

**Rationale:**
1. **Native async**: FastAPI is built on asyncio and ASGI (Starlette) — handles concurrent I/O efficiently
2. **Pydantic v2**: Schema validation with Rust-backed performance. Every API model is also a validated data contract
3. **OpenAPI auto-generation**: Swagger UI and ReDoc out of the box, always synchronized with code
4. **ML/AI ecosystem**: Python is the lingua franca of ML — embedding models, LLM clients, graph analytics all have Python SDKs
5. **Developer productivity**: Decorator-based routing, dependency injection, type hints throughout
6. **Community**: FastAPI is the most-starred Python web framework on GitHub

## Consequences

### Positive
- OpenAPI docs are always current (auto-generated from code annotations)
- Pydantic models serve as both API schema and domain model
- Full async support for all backing services (asyncpg, redis-py, qdrant-client)
- Python ecosystem enables rapid integration with ML tools

### Negative
- Python GIL limits CPU-bound parallelism (not a concern for I/O-bound knowledge platform)
- Python 3.11 startup time is slower than Go or Java for cold starts (mitigate with Kubernetes)
- Type safety is not as strict as Go or Java

### Neutral
- TypeScript SDK is generated from OpenAPI spec for frontend/agent consumers
- Python SDK is generated from OpenAPI spec for Python consumers (not the FastAPI code itself)

## Alternatives Considered

### Alternative 1: Go + Gin
**Why rejected:** Excellent performance, but Python's ML ecosystem advantage outweighs Go's speed advantage for this platform's use case.

### Alternative 2: Java + Spring Boot
**Why rejected:** Verbose, slower development velocity, less natural fit for ML integration.

### Alternative 3: Django REST Framework
**Why rejected:** Synchronous by default. ORM coupling makes it harder to use async backends.

## References
- [ADR-001](ADR-001-api-first-architecture.md) — API-First requires OpenAPI generation
