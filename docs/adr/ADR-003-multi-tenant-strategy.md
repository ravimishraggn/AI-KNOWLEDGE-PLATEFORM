# ADR-003: Multi-Tenant Strategy — Schema-per-Tenant with Shared Infrastructure

## Status
Accepted

## Date
2025-05-31

## Context

The platform must support multiple deployment models:
- **Single tenant** (small team, on-premise)
- **Department-scoped** (business unit isolation within one org)
- **Enterprise SaaS** (full multi-tenant, hundreds of tenants)
- **Multi-region** (data sovereignty requirements)

Three standard multi-tenancy patterns exist:
1. **Database-per-tenant**: Full isolation, highest cost, complex operations
2. **Schema-per-tenant**: Strong isolation, shared infrastructure, moderate complexity
3. **Row-level-security (RLS)**: Shared everything, lowest cost, highest risk if misconfigured

## Decision

The platform uses **Schema-per-tenant** as the default strategy with **Row-Level Security** as the enforcement mechanism at the query layer:

1. Each tenant gets a **dedicated PostgreSQL schema** (`tenant_{id}`)
2. All queries are enforced through **Row Level Security** policies
3. `tenant_id` is a **required field** on every domain model
4. API middleware validates tenant context on every request
5. The Control Plane manages tenant provisioning and schema lifecycle
6. **Vector collections** in Qdrant are namespaced by `tenant_id`
7. **OpenSearch indices** are prefixed with `tenant_{id}_`
8. **Graph databases** (Kuzu) use separate database files per tenant in development; namespace isolation in production

### Tenant Context Propagation
```
HTTP Request → Auth Middleware → Extract tenant_id → Bind to request context
→ All DB queries → All event emissions → All cache keys → All log entries
```

## Consequences

### Positive
- Strong isolation: a bug in tenant A cannot expose tenant B's data
- Schema migration per tenant: can roll out changes progressively
- Tenant-specific customizations (config, plugins, ontologies) are natural
- Meets data sovereignty requirements (tenant schemas can be in different regions)

### Negative
- Schema proliferation: 1000 tenants = 1000 schemas (manageable with schema management tooling)
- Cross-tenant analytics requires a separate aggregation layer
- More complex migrations (must run against all tenant schemas)
- Higher memory footprint for connection pooling

### Neutral
- PgBouncer for connection pooling is mandatory at scale
- Tenant onboarding time: ~30 seconds for schema provisioning

## Alternatives Considered

### Alternative 1: Database-per-Tenant
**Why rejected:** Prohibitive cost and operational overhead at scale. Connection limits make this impractical beyond ~100 tenants.

### Alternative 2: Row-Level Security Only (Shared Schema)
**Why rejected:** Single point of failure: a misconfigured policy exposes all tenants. Harder to provide tenant-specific customizations. Regulatory risk.

### Alternative 3: Separate Deployments per Tenant
**Why rejected:** Not SaaS. Defeats the purpose of a shared platform. Use case covered by single-tenant deployment profile.

## References
- [ADR-020](ADR-020-data-sovereignty.md) — Sovereignty builds on tenant isolation
- [Control Plane](../../18-control-plane/) — Tenant lifecycle management
