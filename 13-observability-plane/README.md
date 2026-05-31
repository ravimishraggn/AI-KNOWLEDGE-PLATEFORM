# 13 — Observability Plane

The Observability Plane makes the Knowledge Operating Platform **transparent, debuggable, and alertable**. It provides distributed tracing, metrics collection, structured logging, and alert management.

---

## Responsibilities

- Collect and expose Prometheus metrics from all planes
- Provide distributed tracing via OpenTelemetry
- Structured logging with correlation IDs across planes
- Alert rule management and notification routing
- Platform health aggregation dashboard
- SLO/SLI tracking for search, ingestion, and retrieval latency
- Knowledge quality metrics (freshness, completeness, accuracy)

---

## Three Pillars

### Metrics
- Prometheus scraping endpoint on all planes (`/metrics`)
- Custom KOP metrics: ingestion rate, search latency, graph query time, RAG quality
- Platform SLI: p50/p95/p99 latency per endpoint

### Tracing
- OpenTelemetry SDK in all planes
- Cross-plane trace propagation via `traceparent` header
- Jaeger or AWS X-Ray as trace backends (pluggable)
- Trace sampling configurable per tenant

### Logging
- JSON structured logging (structlog)
- Correlation ID: `request_id`, `trace_id`, `tenant_id`, `user_id`
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Log routing: stdout (container) → aggregation (Loki / CloudWatch)

---

## Key Platform Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `kop_ingestion_total` | Counter | Total documents ingested |
| `kop_ingestion_failed_total` | Counter | Failed ingestions |
| `kop_search_latency_seconds` | Histogram | Search endpoint latency |
| `kop_rag_retrieval_latency_seconds` | Histogram | RAG retrieval latency |
| `kop_graph_query_latency_seconds` | Histogram | Graph query latency |
| `kop_vector_upsert_total` | Counter | Vectors upserted |
| `kop_governance_denials_total` | Counter | Authorization denials |
| `kop_active_tenants` | Gauge | Active tenant count |

---

## Plane Dependencies

- **01-foundation**: metrics emitted from foundation middleware
- All other planes emit metrics and traces through the OpenTelemetry SDK
