# Reference Architecture: Multi-Tenant SaaS Knowledge Platform

## Overview

A production reference architecture for deploying the Knowledge Operating Platform as a **managed, multi-tenant SaaS service** — serving hundreds or thousands of tenant organizations from a single platform deployment.

---

## Target Use Cases

This architecture is used when KOP itself is the product:
- ISVs building knowledge platform products on top of KOP
- Enterprise IT departments building shared internal knowledge services
- SaaS companies embedding knowledge capabilities into their product

---

## Multi-Tenancy Design

### Tenant Tiers

| Tier | Isolation Level | Resources |
|------|----------------|-----------|
| **Free** | Row-level isolation | Shared compute, shared storage bucket (prefix-isolated) |
| **Starter** | Schema-per-tenant | Shared compute, dedicated storage bucket |
| **Professional** | Schema-per-tenant + dedicated vector collection | Dedicated compute namespace |
| **Enterprise** | Full isolation option | Dedicated compute, dedicated vector cluster |
| **Sovereign** | Physical isolation | Dedicated region deployment |

### Tenant Onboarding Flow

```
New Tenant Signup
    → Control Plane: validate and create tenant record
    → PostgreSQL: create tenant_<id> schema
    → S3: create tenant bucket (or prefix in shared bucket)
    → Qdrant: create tenant collections
    → OpenSearch: create tenant index prefix
    → Configure tier limits and feature flags
    → Emit TenantProvisionedEvent
    → Notify tenant (webhook + email)
```

---

## Scalability Architecture

```
Load Balancer (ALB)
    → API Gateway (rate limiting, tenant routing)
    → API Plane (stateless, horizontal scale)
        → Search Plane (stateless, horizontal scale)
        → AI Consumption Plane (stateless, horizontal scale)
        → Ingestion Workers (queue-based, auto-scale)
    → Shared Data Layer:
        PostgreSQL (pgBouncer pool, read replicas)
        Redis Cluster (5 shards)
        OpenSearch Cluster (6 data nodes)
        Qdrant Cluster (3+ nodes)
```

### Scaling Triggers

| Metric | Scale Out Trigger |
|--------|-----------------|
| API latency P95 > 500ms | +2 API pods |
| Ingestion queue depth > 1000 | +4 ingestion workers |
| Search query rate > 1000/s/node | +2 search pods |
| Vector store CPU > 70% | +1 Qdrant node |

---

## Metering and Billing

The Control Plane tracks usage per tenant for billing integration:

```
Usage Metrics:
├── Documents ingested (count + GB)
├── Vector embeddings stored (count + dimensions)
├── Search queries executed (count + type)
├── AI context requests (count + tokens)
├── Agent tool calls (count + tool_name)
├── Knowledge graph nodes (count)
└── API calls (count + endpoint)
```

---

## Operations

### Tenant Isolation Verification

Automated daily test: create two tenants, insert test data in tenant A, verify it is not accessible from tenant B. Any failure triggers immediate alert and platform freeze.

### Tenant Offboarding

```
1. Deactivate API access
2. Export tenant data (per GDPR right to portability)
3. Delete tenant schema (per GDPR right to erasure)
4. Delete storage bucket/prefix
5. Delete vector collections
6. Audit log: retain for 7 years (regulatory)
```

---

## SLA Targets

| Metric | Target |
|--------|--------|
| API availability | 99.9% |
| Search latency P99 | < 500ms |
| Ingestion throughput | > 1,000 docs/min |
| Tenant provisioning | < 60 seconds |
| Data isolation: zero cross-tenant leakage | 100% |
