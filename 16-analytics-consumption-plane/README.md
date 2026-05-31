# 16 — Analytics Consumption Plane

The Analytics Consumption Plane delivers **semantic analytics** — business metrics grounded in the platform's ontology, natural language queries over knowledge assets, and governed analytical views.

---

## Responsibilities

- Define and compute semantic business metrics (grounded in ontology terms)
- Provide natural language query interface over knowledge assets
- Expose pre-built analytical views for platform-registered domains
- Integrate with BI tools via semantic layer APIs
- Track metric definitions with lineage (a metric is a governed asset)

---

## Core Concepts

| Concept | Description |
|---------|-------------|
| **SemanticMetric** | A business metric with an ontology-grounded definition |
| **MetricRegistry** | Registry of all defined metrics with owners and lineage |
| **NLQuery** | Natural language query translated to structured retrieval |
| **AnalyticsView** | A governed, reusable analytical perspective on knowledge |

---

## Semantic Metric Example

```
SemanticMetric:
  name: "credit_exposure_by_counterparty"
  domain: "banking.risk"
  definition: "Total credit exposure aggregated by canonical counterparty entity"
  ontology_term: "fibo:CreditExposure"
  computation: "SUM(exposure_amount) GROUP BY canonical_entity_id"
  governed: true
  owner: "risk_analytics_team"
```

---

## Natural Language Analytics

```
POST /v1/analytics/nl-query
{
  "query": "What is our total credit exposure to European banks as of Q1 2025?",
  "domain": "banking.risk"
}

→ Translates to:
  - Entity resolution: "European banks" → canonical entity set
  - Semantic metric: "credit_exposure_by_counterparty"
  - Time filter: Q1 2025
  → Returns structured result with citations
```

---

## Plane Dependencies

- **07-semantic**: metric definitions use glossary terms
- **05-ontology**: metrics reference ontology concepts
- **08-knowledge-graph**: entity aggregation via graph traversal
- **11-governance**: metric access control
