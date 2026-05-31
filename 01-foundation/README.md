# 01 — Foundation Plane

The Foundation Plane is the platform's lowest layer. It provides **shared primitives, contracts, and infrastructure abstractions** that every other plane depends on. Nothing in the Foundation has business logic. Everything in the Foundation is reused by 2+ planes.

---

## Responsibilities

| Component | Responsibility |
|-----------|---------------|
| **FastAPI Application** | Platform entry point, ASGI server, middleware stack |
| **Configuration Framework** | Environment-based config with validation |
| **Plugin Registry** | Discovers and loads registered plugins at startup |
| **Event Bus** | Redis Streams producer/consumer abstraction |
| **Auth Abstraction** | Pluggable authentication middleware |
| **Storage Abstraction** | Cloud-neutral object storage interface |
| **Shared Models** | Base Pydantic models used across all planes |
| **Shared Events** | Platform-wide CloudEvents-compatible event schemas |
| **Middleware** | Tenant context, request ID, CORS, logging |
| **Health Checks** | Liveness and readiness probes |

---

## Module Structure

```
src/knowledge_platform/
├── main.py                    # FastAPI application factory
├── config/
│   ├── settings.py            # Pydantic settings model
│   └── loader.py              # Environment + file config loading
├── models/
│   ├── base.py                # BaseModel with tenant_id, timestamps
│   ├── tenant.py              # Tenant domain model
│   ├── pagination.py          # Cursor/offset pagination models
│   └── responses.py           # Standard API response envelopes
├── events/
│   ├── bus.py                 # EventBus interface + Redis implementation
│   ├── contracts.py           # All platform event schemas
│   └── consumer.py            # Consumer group management
├── plugins/
│   ├── registry.py            # Plugin discovery and loading
│   ├── base.py                # PluginBase ABC
│   └── types.py               # Plugin capability type registry
├── auth/
│   ├── abstract.py            # AuthProvider interface
│   ├── jwt.py                 # JWT reference implementation
│   └── middleware.py          # Request authentication middleware
├── storage/
│   ├── abstract.py            # StorageInterface ABC
│   ├── s3.py                  # AWS S3 adapter
│   ├── azure_blob.py          # Azure Blob adapter
│   └── local.py               # Local filesystem adapter (dev)
├── api/
│   ├── router.py              # Root API router
│   ├── health.py              # Health check endpoints
│   └── middleware.py          # Tenant context middleware
├── core/
│   ├── exceptions.py          # Platform exception hierarchy
│   ├── logging.py             # Structured logging setup
│   └── tracing.py             # OpenTelemetry setup
└── middleware/
    ├── tenant.py              # Tenant context extraction
    ├── request_id.py          # Request ID propagation
    └── governance.py          # Governance hooks
```

---

## Key Interfaces

### PluginBase
Every plugin implements `PluginBase` and declares its capabilities.

### AuthProvider
Pluggable authentication. Default: JWT. Adapters: OIDC, API Key.

### EventBus
Async event publishing and subscription. Default: Redis Streams. Adapter: Kafka.

### StorageInterface
Cloud-neutral object storage. Default: S3. Adapters: Azure Blob, GCS, Local.

See [interfaces.md](docs/interfaces.md) for full contract specifications.

---

## Configuration

All configuration is driven by environment variables, validated by Pydantic Settings:

```bash
KOP_ENV=production
KOP_DB_URL=postgresql+asyncpg://user:pass@host:5432/db
KOP_REDIS_URL=redis://host:6379
KOP_SECRET_KEY=...
KOP_TENANT_MODE=multi
KOP_PLUGIN_SCAN=true
```

See [docs/configuration.md](docs/configuration.md) for full reference.

---

## Extension Points

- **Auth Provider**: implement `AuthProvider` and register via entry point `kop.auth`
- **Storage Adapter**: implement `StorageInterface` and register via `kop.storage`
- **Event Bus Adapter**: implement `EventBusInterface` and register via `kop.events`
- **Middleware**: add custom middleware to the FastAPI middleware stack

---

## Dependencies

The Foundation Plane depends on:
- PostgreSQL (via asyncpg)
- Redis (via redis-py async)
- No other planes

All other planes depend on the Foundation Plane.
