# Build Roadmap — Knowledge Operating Platform

## Roadmap Philosophy

The platform is built **plane by plane**, not feature by feature. Each phase delivers a **working vertical slice** — a set of planes that can be deployed together and provide real value. Later phases extend and connect earlier planes.

The roadmap is structured in **7 phases**. Each phase has:
- Objectives
- Deliverables (planes + features)
- Success criteria
- Estimated duration (relative to team size of 2-4 engineers)

---

## Phase 0 — Architecture & Contracts (Current)

**Duration:** 4-6 weeks  
**Status:** In Progress

### Objectives
- Establish the complete repository structure
- Define all interfaces and contracts (no implementation)
- Write all ADRs
- Write all plane documentation
- Align the team on architectural principles

### Deliverables
- [x] Repository structure (20 planes)
- [x] All ADRs (001-020)
- [x] Platform vision documentation
- [x] Build roadmap
- [ ] All plane interface definitions (Python ABCs)
- [ ] All plane documentation (README, architecture, interfaces, extension-points)
- [ ] Event contract schemas
- [ ] Docker Compose for all backing services
- [ ] CI/CD pipeline skeleton

### Success Criteria
- Any developer can clone the repo and understand the full architecture
- All interfaces are defined — implementation can begin in parallel across planes
- Zero ambiguity about cross-plane contracts

---

## Phase 1 — Foundation + Core Data Planes

**Duration:** 8-12 weeks  
**Team:** 2-3 engineers

### Objectives
Build the operational backbone of the platform. By the end of this phase, the platform can ingest documents, extract metadata, and store them in a searchable catalog.

### Planes
- **01-foundation** — FastAPI app, plugin registry, auth middleware, storage abstraction, event bus
- **02-ingestion-plane** — S3 connector, filesystem connector, REST API connector
- **03-metadata-plane** — Metadata harvesting, catalog API, basic enrichment

### Deliverables
- FastAPI application with health, auth, and tenant middleware
- Plugin registry (entry point discovery and loading)
- Redis Streams event bus (producer and consumer)
- S3 ingestion connector with schema-validated pipeline
- PostgreSQL metadata store with tenant isolation
- Automated metadata harvesting on ingestion events
- OpenAPI docs for all endpoints

### Success Criteria
- Document can be uploaded via API → ingested from S3 → metadata harvested → queryable in catalog
- Multi-tenant isolation verified (integration tests)
- Event bus: ingestion event → metadata harvest event
- All connectors are plugins (not hardcoded)

---

## Phase 2 — Knowledge Graph + Vector + Search

**Duration:** 10-14 weeks  
**Team:** 3-4 engineers

### Objectives
Transform the metadata catalog into a queryable, semantically searchable knowledge store.

### Planes
- **08-knowledge-graph-plane** — Kuzu adapter, entity/relationship CRUD, graph query API
- **09-vector-plane** — Qdrant adapter, embedding pipeline, embedding registry
- **10-search-plane** — OpenSearch indexing, keyword search, semantic search, hybrid search

### Deliverables
- Kuzu graph adapter: create nodes, relationships, traverse paths
- Neo4j adapter (structural parity with Kuzu adapter)
- Qdrant adapter: upsert, query, filter
- Chroma adapter (lightweight dev alternative)
- Embedding pipeline: text-embedding-3-large (OpenAI), nomic-embed-text (local)
- OpenSearch indexing pipeline subscribed to ingestion events
- Unified search API: keyword + semantic + hybrid
- Search results respect tenant isolation and governance filters

### Success Criteria
- Knowledge asset searchable via keyword and semantic search within 5 seconds of ingestion
- Graph: entity → relationships → related entities query in < 100ms
- Vector: top-10 semantic search in < 200ms (p99)
- Hybrid search outperforms keyword-only by > 20% on test dataset

---

## Phase 3 — Semantic Intelligence

**Duration:** 8-10 weeks  
**Team:** 2-3 engineers

### Objectives
Add the semantic layer that distinguishes a knowledge platform from a data catalog.

### Planes
- **05-ontology-plane** — OWL/SKOS registry, versioning, validation
- **06-taxonomy-plane** — Hierarchical classification, tagging
- **07-semantic-plane** — Business glossary, governed term authoring
- **04-canonical-plane** — Entity resolution, canonical registry, synonym mapping

### Deliverables
- Ontology registry: import/export Turtle, version management
- SKOS taxonomy import and hierarchy navigation
- Business glossary CRUD with governance workflow (draft → review → publish)
- Canonical entity type registry
- Entity resolution: exact match + fuzzy match via vector similarity
- Synonym mapping for search boost
- Glossary terms linked to ontology concepts and knowledge graph node types

### Success Criteria
- Ontology can be imported in Turtle format and all concepts are queryable
- Business glossary term can be created and goes through full governance workflow
- Entity resolution correctly merges duplicate entities from two source systems (test dataset)
- Search results boosted by glossary term matches

---

## Phase 4 — AI & Agentic Consumption

**Duration:** 8-12 weeks  
**Team:** 2-3 engineers

### Objectives
Turn the knowledge platform into the ground truth for AI workloads.

### Planes
- **14-ai-consumption-plane** — RAG pipelines, context APIs, semantic retrieval
- **15-agent-consumption-plane** — MCP server, knowledge tools, tool registry

### Deliverables
- Basic RAG pipeline: query → vector retrieve → context assemble → return
- Advanced RAG: HyDE, graph-augmented retrieval, structured entity retrieval
- Context API: assemble structured context for any knowledge asset
- MCP Server: HTTP+SSE transport, tenant-aware, governed
- MCP Tools: `kop_search`, `kop_retrieve`, `kop_define`, `kop_classify`, `kop_similar`
- Tool registry: register custom agent tools as plugins
- AI response lineage: record what knowledge grounded each AI response

### Success Criteria
- MCP server can be connected to Claude Desktop with zero custom code
- RAG pipeline reduces hallucination rate by > 50% vs baseline (test set)
- All AI retrievals are logged and lineage-traceable
- Tool calls respect tenant isolation and governance

---

## Phase 5 — Governance & Lineage

**Duration:** 8-10 weeks  
**Team:** 2-3 engineers

### Objectives
Harden the platform for enterprise adoption with full governance and lineage.

### Planes
- **11-governance-plane** — RBAC, ABAC, policy engine (OPA), approval workflows
- **12-lineage-plane** — End-to-end lineage graph, impact analysis
- **13-observability-plane** — Metrics, tracing, alerting, logging

### Deliverables
- Role management API: create/assign/revoke roles
- ABAC policy: data classification + sovereignty zone enforcement
- OPA integration: custom policy evaluation
- Approval workflow: submit → review → approve/reject → execute
- Lineage graph: every ingestion, transformation, embedding, and retrieval traced
- Impact analysis API: "if this asset changes, what downstream assets are affected?"
- OpenTelemetry distributed tracing across all planes
- Prometheus metrics + Grafana dashboards

### Success Criteria
- Unauthorized access to RESTRICTED data returns 403 (100% of test cases)
- Full lineage traceable from raw S3 document to AI response
- Impact analysis returns affected downstream assets in < 500ms
- P99 API latency dashboards operational

---

## Phase 6 — Control Plane & Developer Experience

**Duration:** 6-8 weeks  
**Team:** 2 engineers

### Objectives
Make the platform operable at scale and developer-friendly.

### Planes
- **18-control-plane** — Tenant management, platform configuration, registry governance
- **17-api-plane** — API gateway, rate limiting, versioning
- **19-developer-experience** — CLI, Python SDK, TypeScript SDK, examples

### Deliverables
- Tenant provisioning API: create/configure/deactivate tenants
- Platform configuration API: global + per-tenant settings
- API gateway with rate limiting and usage metering
- API version routing (v1, v2 coexistence)
- `kop` CLI: `kop login`, `kop tenant create`, `kop search`, `kop ingest`
- Python SDK (generated from OpenAPI)
- TypeScript SDK (generated from OpenAPI)
- Example applications: banking search, healthcare knowledge graph, RAG pipeline

### Success Criteria
- New tenant provisioned in < 30 seconds via CLI
- SDK can perform end-to-end search in < 10 lines of code
- API gateway enforces rate limits (integration tests)

---

## Phase 7 — Reference Architectures & Vertical Packs

**Duration:** Ongoing  
**Team:** Architecture + Domain Experts

### Objectives
Accelerate industry adoption with pre-built reference architectures and industry ontologies.

### Deliverables
- Banking Knowledge Platform architecture + FIBO ontology import
- Healthcare Knowledge Platform architecture + SNOMED/ICD-11 import
- Insurance Knowledge Platform architecture + ACORD ontology
- Private Markets Intelligence Platform architecture
- Multi-Tenant SaaS Knowledge Platform architecture
- Industry-specific ingestion connectors (Bloomberg, Refinitiv, Epic EHR, Salesforce)
- Benchmark reports for each reference architecture

---

## Dependency Map

```
Phase 0 (Architecture)
    └── Phase 1 (Foundation + Ingestion + Metadata)
            ├── Phase 2 (Graph + Vector + Search)
            │       └── Phase 3 (Semantic Intelligence)
            │               └── Phase 4 (AI & Agentic)
            ├── Phase 5 (Governance + Lineage) [parallel with Phase 2-4]
            └── Phase 6 (Control + DevEx) [parallel with Phase 4-5]
                        └── Phase 7 (Reference Architectures) [ongoing]
```

---

## Versioning Strategy

| Release | Content | Stability |
|---------|---------|-----------|
| 0.x | Phases 0-1: Foundation | Experimental |
| 0.2 | Phase 2: Graph + Vector + Search | Beta |
| 0.3 | Phase 3: Semantic | Beta |
| 0.5 | Phase 4: AI & Agentic | RC |
| 0.8 | Phase 5: Governance | RC |
| 1.0 | Phase 6: Control + DevEx | GA |
| 1.x | Phase 7: Verticals | GA + Extensions |
