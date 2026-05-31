# Foundation Plane — Architecture

## Overview

The Foundation Plane is a Python package (`knowledge_platform`) that provides all shared infrastructure for the Knowledge Operating Platform. It is not a standalone service — it is the backbone that other planes import and extend.

The Foundation creates the **FastAPI application factory**, **configures middleware**, **discovers plugins**, and provides **abstract interfaces** for every swappable infrastructure component.

---

## Application Bootstrap

```
startup sequence:
1. Load configuration (Pydantic Settings from environment)
2. Initialize structured logging (JSON in production)
3. Initialize OpenTelemetry tracing
4. Connect to PostgreSQL (asyncpg connection pool)
5. Connect to Redis (async connection pool)
6. Discover and register plugins (entry point scanning)
7. Initialize Auth middleware
8. Initialize Tenant middleware
9. Mount plane routers (dynamic, based on enabled planes)
10. Register health check endpoints
11. Emit PlatformStartedEvent
```

---

## Middleware Stack (Request Order)

```
HTTP Request
    → CORS Middleware
    → Request ID Middleware (inject X-Request-ID)
    → Logging Middleware (structured request/response logging)
    → Authentication Middleware (validate token, extract identity)
    → Tenant Middleware (extract tenant_id, bind to context)
    → OpenTelemetry Middleware (trace context propagation)
    → Rate Limit Middleware (pluggable, default: none in dev)
    → Route Handler
    → Response
```

---

## Plugin System Architecture

```
Plugin Package (published to PyPI)
    → declares entry point in pyproject.toml:
        [project.entry-points."kop.connectors"]
        my_connector = "my_package:MyConnectorClass"

Platform Startup
    → PluginRegistry.scan()
    → importlib.metadata.entry_points(group="kop.connectors")
    → loads and validates each plugin class
    → registers in PluginRegistry under capability type

Consumer (e.g., Ingestion Plane)
    → registry.get("connector", "my_connector")
    → returns configured plugin instance
```

---

## Event Bus Architecture

```
Producer (any plane)
    → event_bus.publish(event: PlatformEvent)
    → serializes to JSON (CloudEvents envelope)
    → XADD to Redis Stream: kop.{plane}.{entity}.{action}.v1

Consumer (any plane)
    → event_bus.subscribe(stream, group, handler)
    → XREADGROUP from Redis Stream
    → deserializes from JSON
    → calls handler(event)
    → ACKs on successful processing
    → Dead-letter queue on repeated failure
```

---

## Tenant Context Architecture

Every request carries a `TenantContext`:

```
TenantContext:
    tenant_id: UUID
    tenant_slug: str
    db_schema: str          # "tenant_{slug}"
    storage_bucket: str     # tenant-specific storage bucket
    sovereignty_zone: str   # EU | US | APAC | UK
    feature_flags: dict     # tenant-specific feature overrides
```

The context is set per-request in a `contextvars.ContextVar` and is available to all downstream code without explicit parameter passing.

---

## Error Handling Architecture

All platform exceptions inherit from `KOPException`:

```
KOPException
├── AuthenticationError (401)
├── AuthorizationError (403)
├── TenantNotFoundError (404)
├── ValidationError (422)
├── ConflictError (409)
├── PlaneDependencyError (503)
└── PluginError (500)
```

FastAPI exception handlers convert KOPExceptions to standard JSON error responses with request_id, error_code, and human-readable message.

---

## Configuration Architecture

```
PlatformSettings (Pydantic BaseSettings)
├── DatabaseConfig
├── RedisConfig
├── AuthConfig (selects auth provider)
├── StorageConfig (selects storage adapter)
├── EventBusConfig (selects event bus adapter)
├── ObservabilityConfig
└── TenantConfig (single vs multi-tenant mode)
```

All config values come from environment variables. No config files in production. `.env` files for local development only.

---

## Health Check Architecture

```
GET /health/live     → liveness probe (is the process running?)
GET /health/ready    → readiness probe (are dependencies ready?)
GET /health/startup  → startup probe (did initialization complete?)
GET /health/detailed → full dependency status (authenticated endpoint)
```

Readiness checks: PostgreSQL connection, Redis connection, plugin registry loaded.
