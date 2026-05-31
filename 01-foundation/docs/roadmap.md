# Foundation Plane — Roadmap

## Current State (Phase 0)
Interface definitions, documentation, and directory structure. No implementation.

---

## Phase 1 Deliverables (v0.1)

- [ ] FastAPI application factory (`create_app()`)
- [ ] Pydantic Settings configuration (`PlatformSettings`)
- [ ] Structured JSON logging (structlog)
- [ ] Asyncpg connection pool with tenant-schema routing
- [ ] Redis connection pool
- [ ] `TenantScopedModel` and `PlatformEvent` base models
- [ ] JWT `AuthProvider` reference implementation
- [ ] Redis Streams `EventBusInterface` implementation
- [ ] S3 `StorageInterface` implementation
- [ ] Local filesystem `StorageInterface` (dev/test)
- [ ] Plugin registry: entry point scanning and loading
- [ ] Tenant context middleware
- [ ] Request ID middleware
- [ ] Health check endpoints (`/health/live`, `/health/ready`)
- [ ] Standard error response handling
- [ ] Unit tests: all interfaces tested against mock implementations
- [ ] Integration tests: PostgreSQL, Redis connections

## Phase 2 Additions (v0.2)

- [ ] OpenTelemetry distributed tracing integration
- [ ] OIDC `AuthProvider` adapter (Auth0, Okta, Azure AD)
- [ ] Kafka `EventBusInterface` adapter
- [ ] Azure Blob `StorageInterface` adapter
- [ ] GCS `StorageInterface` adapter
- [ ] Prometheus metrics endpoint (`/metrics`)
- [ ] Rate limiting middleware (plugin)
- [ ] API key `AuthProvider` adapter
- [ ] Dead-letter queue handling for event bus

## Phase 3+ Additions (v0.3+)

- [ ] Tenant provisioning hooks (called by Control Plane)
- [ ] Plugin health aggregation in `/health/detailed`
- [ ] Config schema validation UI
- [ ] Event schema registry integration
- [ ] Streaming responses for large payloads
- [ ] WebSocket support for real-time events

---

## Stability Guarantees

| Component | Stability |
|-----------|-----------|
| `AuthProvider` interface | Stable from v0.1 |
| `StorageInterface` interface | Stable from v0.1 |
| `EventBusInterface` interface | Stable from v0.1 |
| `PluginBase` interface | Stable from v0.1 |
| `TenantScopedModel` fields | Stable from v0.1 |
| `PlatformEvent` schema | Stable from v0.1 |
| Internal implementation details | May change across minor versions |
