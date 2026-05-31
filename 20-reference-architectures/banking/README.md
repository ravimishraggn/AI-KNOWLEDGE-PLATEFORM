# Reference Architecture: Banking Knowledge Platform

## Overview

A production reference architecture for deploying the Knowledge Operating Platform in a **banking or financial services** organization. Covers the core knowledge infrastructure for: regulatory compliance, credit risk, counterparty management, and AI-powered research.

---

## Target Use Cases

| Use Case | KOP Capability |
|----------|---------------|
| **Regulatory Knowledge Base** | Ingest regulations → ontology → governed AI Q&A |
| **Credit Risk Intelligence** | Counterparty graph → risk exposure queries |
| **KYC/AML Entity Resolution** | Canonical entity resolution across source systems |
| **Investment Research AI** | Semantic search + RAG over research documents |
| **Product Knowledge Graph** | Financial product ontology + relationship graph |
| **Compliance Documentation AI** | Policy documents → governed RAG → compliance Q&A |

---

## Recommended Platform Configuration

### Planes Active

All 20 planes active. Priority order for initial deployment:

1. **Foundation** (prerequisite)
2. **Ingestion** — Bloomberg, Refinitiv, SharePoint, S3
3. **Metadata** — Auto-harvest from all ingested sources
4. **Ontology** — Import FIBO (Financial Industry Business Ontology)
5. **Canonical** — Entity resolution for counterparties, instruments, issuers
6. **Knowledge Graph** — Counterparty + instrument + exposure graph
7. **Semantic** — Regulatory term glossary (Basel III, DORA, MiFID II)
8. **Vector** — Research document embeddings
9. **Search** — Hybrid search for research and compliance
10. **Governance** — RBAC, data classification, GDPR/sovereignty
11. **AI Consumption** — Regulatory Q&A, research assistant
12. **Agent Consumption** — Risk analyst agent tools

### Data Classification

| Data Type | Classification | Sovereignty |
|-----------|---------------|-------------|
| Published research | INTERNAL | US/EU |
| Counterparty PII | RESTRICTED | Jurisdiction-bound |
| Risk exposure data | CONFIDENTIAL | Tenant-bound |
| Regulatory docs | INTERNAL | US/EU/UK |
| Deal terms | RESTRICTED | Jurisdiction-bound |

---

## Industry Ontologies

### FIBO (Financial Industry Business Ontology)

FIBO is the primary domain ontology for banking deployments:
- `fibo:CreditAgreement`, `fibo:LoanContract`, `fibo:SecurityIdentifier`
- `fibo:Organisation`, `fibo:LegalEntity`, `fibo:FinancialInstitution`
- `fibo:Exposure`, `fibo:CreditRisk`, `fibo:MarketRisk`

**Import process:**
```bash
kop ontology import fibo-complete.ttl --format turtle --domain banking
kop ontology publish <fibo-ontology-id>
```

### Regulatory Ontology (Custom)

Platform-specific regulatory concept ontology:
- Basel III concepts: capital adequacy, leverage ratio, liquidity coverage
- DORA concepts: ICT risk, operational resilience, incident reporting
- MiFID II concepts: best execution, transaction reporting, market data

---

## Graph Model (Banking)

```
(LegalEntity)-[COUNTERPARTY_OF]->(LegalEntity)
(LegalEntity)-[HAS_EXPOSURE {amount, currency, date}]->(LegalEntity)
(FinancialInstrument)-[ISSUED_BY]->(LegalEntity)
(LegalEntity)-[REGULATED_BY]->(RegulatoryAuthority)
(LegalEntity)-[SUBSIDIARY_OF]->(LegalEntity)
(Jurisdiction)-[GOVERNS]->(LegalEntity)
(RegulatoryCapital)-[REQUIRED_BY]->(RegulatoryAuthority)
```

---

## Recommended Technology Configuration

| Component | Banking Config |
|-----------|---------------|
| **Graph** | Neo4j Enterprise (distributed, large graph) |
| **Vector** | Qdrant (sovereign deployment, EU tenants → EU cluster) |
| **Search** | OpenSearch (on-premise or AWS OpenSearch) |
| **Auth** | OIDC → Active Directory / Okta |
| **Storage** | AWS S3 with S3 Object Lock (immutable audit trail) |
| **Event Bus** | Apache Kafka (high-volume trade/risk events) |
| **Cloud** | AWS (primary), with data sovereignty enforcement |

---

## Compliance Considerations

- **GDPR**: EU customer data in EU-sovereign Qdrant collection and PostgreSQL schema
- **BCBS 239**: Data lineage is platform-native (satisfies risk data aggregation requirements)
- **DORA**: Operational resilience requires multi-AZ deployment, documented RTO/RPO
- **MiFID II**: Transaction-linked knowledge assets must have 7-year retention
- **SOC 2**: Audit log (lineage plane) provides Type II evidence

---

## Deployment Architecture

```
Internet
    → WAF → API Gateway → KOP API Plane
                              ├── Ingestion Plane (ECS/EKS)
                              ├── Search Plane (ECS/EKS)
                              ├── AI Consumption Plane (ECS/EKS)
                              └── Agent Consumption Plane (ECS/EKS)
                                         │
                          ┌──────────────┼──────────────┐
                          ▼              ▼              ▼
                      RDS (PG)    ElastiCache      OpenSearch
                      (tenant      (Redis)          Service
                       schemas)
                          │
                    ┌─────┴─────┐
                    ▼           ▼
                 Qdrant       Neo4j
               (Sovereign)  (Graph DB)
```

---

## Getting Started (Banking)

```bash
# 1. Clone and start platform
git clone https://github.com/your-org/knowledge-operating-platform
docker-compose up -d

# 2. Create banking tenant
kop tenant create --name "acme-bank" --domain "banking" \
  --sovereignty-zone EU --classification-default INTERNAL

# 3. Import FIBO ontology
kop ontology import fibo-complete.ttl --tenant acme-bank --publish

# 4. Configure SharePoint connector
kop connector configure sharepoint --tenant acme-bank \
  --site-url https://acme.sharepoint.com/sites/compliance

# 5. Start ingestion
kop ingest sharepoint --tenant acme-bank --path "/Shared Documents/Regulatory/"

# 6. Run semantic search
kop search "Basel III capital adequacy requirements" --tenant acme-bank
```
