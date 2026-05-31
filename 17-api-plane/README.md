# 17 — API Plane

The API Plane is the **unified gateway** to the Knowledge Operating Platform. It provides API versioning, rate limiting, usage metering, and the unified API surface that external consumers interact with.

---

## Responsibilities

- Unified API routing across all planes
- API versioning (v1, v2 coexistence with deprecation windows)
- Rate limiting per tenant, per user, per endpoint
- Usage metering and quota enforcement
- API key management for service accounts
- API documentation portal (auto-generated OpenAPI)
- Request/response transformation for API version compatibility

---

## API Surface

All platform APIs are available under `/api/v{version}/`:

```
/api/v1/
├── /ingest/         → Ingestion Plane APIs
├── /metadata/       → Metadata Plane APIs
├── /canonical/      → Canonical Plane APIs
├── /ontology/       → Ontology Plane APIs
├── /taxonomy/       → Taxonomy Plane APIs
├── /semantic/       → Semantic Plane APIs
├── /graph/          → Knowledge Graph Plane APIs
├── /vector/         → Vector Plane APIs
├── /search/         → Search Plane APIs
├── /governance/     → Governance Plane APIs
├── /lineage/        → Lineage Plane APIs
├── /ai/             → AI Consumption Plane APIs
├── /agent/          → Agent Consumption Plane APIs (MCP)
├── /analytics/      → Analytics Plane APIs
└── /admin/          → Control Plane APIs
```

---

## Versioning Strategy

- Semantic versioning for the API surface
- Breaking changes require a new major version (`v1` → `v2`)
- Old versions deprecated with 90-day notice and sunset date
- Version routing: `Accept: application/vnd.kop.v2+json`

---

## Rate Limiting

Default limits (configurable per tenant):
```
Anonymous:  100 req/min
Reader:     1,000 req/min
Analyst:    5,000 req/min
AI Agent:   10,000 req/min
Admin:      unlimited
```

---

## Plane Dependencies

- **01-foundation**: auth, tenant middleware
- **11-governance**: request authorization
- Routes to all other planes
