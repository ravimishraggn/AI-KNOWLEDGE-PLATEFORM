# End-to-End Flow: Private Markets Intelligence Platform
## Multi-Tenant SaaS on the Knowledge Operating Platform

> **Platform:** iLevel-style Portfolio Monitoring SaaS  
> **Problem:** Same financial metrics (IRR, MOIC, DPI, Valuation) live in every client's database under completely different column names and table structures. No cross-client query is possible today.  
> **Solution:** The Knowledge Operating Platform creates a semantic, canonical, and AI-queryable knowledge layer on top of every client's isolated SQL Server database.

---

## Table of Contents

1. [The Problem in Detail](#1-the-problem-in-detail)
2. [Platform Tenant Architecture](#2-platform-tenant-architecture)
3. [Plane-by-Plane Flow with Sample Data](#3-plane-by-plane-flow-with-sample-data)
   - [Plane 1 — Ingestion](#plane-1--ingestion-plane)
   - [Plane 2 — Metadata](#plane-2--metadata-plane)
   - [Plane 3 — Canonical](#plane-3--canonical-plane)
   - [Plane 4 — Ontology](#plane-4--ontology-plane)
   - [Plane 5 — Taxonomy](#plane-5--taxonomy-plane)
   - [Plane 6 — Semantic](#plane-6--semantic-plane)
   - [Plane 7 — Knowledge Graph](#plane-7--knowledge-graph-plane)
   - [Plane 8 — Vector](#plane-8--vector-plane)
   - [Plane 9 — Search](#plane-9--search-plane)
   - [Plane 10 — Governance](#plane-10--governance-plane)
   - [Plane 11 — Lineage](#plane-11--lineage-plane)
   - [Plane 12 — Observability](#plane-12--observability-plane)
   - [Plane 13 — AI Consumption](#plane-13--ai-consumption-plane)
   - [Plane 14 — Agent Consumption](#plane-14--agent-consumption-plane)
4. [End-to-End Query Walkthrough](#4-end-to-end-query-walkthrough)
5. [What This Unlocks](#5-what-this-unlocks)

---

## 1. The Problem in Detail

### Three Real Clients. Same Metrics. Completely Different Names.

The platform serves private equity fund managers. Every fund manager tracks the same performance metrics — **IRR, MOIC, DPI, TVPI, NAV, Valuation, Invested Capital** — but each has built their own SQL Server database independently. The result: identical concepts, zero interoperability.

---

### Client A — "Apex Capital Partners"

```sql
-- Database: apex_capital_db
-- Table: fund_performance
CREATE TABLE fund_performance (
    fund_id         VARCHAR(20) PRIMARY KEY,
    fund_name       VARCHAR(200),
    irr_net         DECIMAL(8,4),      -- ← Net IRR
    irr_gross       DECIMAL(8,4),      -- ← Gross IRR
    moic            DECIMAL(6,2),      -- ← Multiple on Invested Capital
    dpi             DECIMAL(6,2),      -- ← Distributions to Paid-In
    tvpi            DECIMAL(6,2),      -- ← Total Value to Paid-In
    nav_usd         BIGINT,            -- ← Net Asset Value (USD)
    reporting_date  DATE
);

-- Table: portfolio_companies
CREATE TABLE portfolio_companies (
    company_id          VARCHAR(20) PRIMARY KEY,
    company_name        VARCHAR(200),
    sector              VARCHAR(100),
    geography           VARCHAR(100),
    entry_date          DATE,
    cost_basis_usd      BIGINT,        -- ← Invested Capital
    current_valuation_usd BIGINT       -- ← Fair Market Value
);

-- Sample data
INSERT INTO fund_performance VALUES
('APX-F1', 'Apex Growth Fund I', 0.2340, 0.2890, 2.45, 1.20, 2.45, 485000000, '2024-12-31'),
('APX-F2', 'Apex Buyout Fund II', 0.1820, 0.2410, 1.98, 0.85, 1.98, 312000000, '2024-12-31');

INSERT INTO portfolio_companies VALUES
('APX-PC-001', 'TechFlow Inc',       'Software',    'North America', '2021-03-15', 45000000, 112000000),
('APX-PC-002', 'MedCore Solutions',  'Healthcare',  'Europe',        '2020-07-01', 62000000, 98000000),
('APX-PC-003', 'GreenEnergy Co',     'Clean Energy','North America', '2022-01-10', 28000000, 41000000);
```

---

### Client B — "Blue Ridge Ventures"

```sql
-- Database: blueridge_db
-- Table: portfolio_returns  (same concept, different name, different structure)
CREATE TABLE portfolio_returns (
    portfolio_id        INT PRIMARY KEY,
    portfolio_name      VARCHAR(200),
    net_irr_pct         FLOAT,         -- ← Net IRR (same as irr_net above!)
    gross_irr_pct       FLOAT,         -- ← Gross IRR
    return_multiple     FLOAT,         -- ← MOIC
    distribution_ratio  FLOAT,         -- ← DPI
    total_value_ratio   FLOAT,         -- ← TVPI
    fair_value          MONEY,         -- ← NAV (same as nav_usd!)
    as_of_date          DATETIME
);

-- Table: investee_companies  (same as portfolio_companies above)
CREATE TABLE investee_companies (
    investee_id         INT PRIMARY KEY,
    investee_name       VARCHAR(200),
    industry_sector     VARCHAR(100),
    country             VARCHAR(100),
    investment_date     DATE,
    amount_invested     MONEY,         -- ← Invested Capital
    mark_to_market      MONEY          -- ← Fair Market Value
);

-- Sample data
INSERT INTO portfolio_returns VALUES
(1, 'BRV Core Fund 2019',   0.197, 0.251, 2.12, 0.90, 2.12, 278000000, '2024-12-31'),
(2, 'BRV Growth Fund 2021', 0.231, 0.298, 1.75, 0.30, 1.75, 195000000, '2024-12-31');

INSERT INTO investee_companies VALUES
(101, 'DataStream Analytics', 'Technology',   'United States', '2020-11-20', 38000000, 91000000),
(102, 'PharmaLink Corp',      'Life Sciences', 'Germany',       '2019-05-15', 55000000, 87000000),
(103, 'AutoServ Holdings',    'Industrials',   'United Kingdom','2021-08-30', 42000000, 63000000);
```

---

### Client C — "Citadel Growth Fund"

```sql
-- Database: citadel_gf_db
-- Table: fund_metrics  (yet another name, yet another structure)
CREATE TABLE fund_metrics (
    metric_id                        INT PRIMARY KEY,
    fund_code                        NVARCHAR(50),
    internal_rate_return_net         NUMERIC(10,6), -- ← Net IRR (third naming!)
    internal_rate_return_gross       NUMERIC(10,6), -- ← Gross IRR
    money_on_money                   NUMERIC(8,4),  -- ← MOIC
    distributions_over_contributions NUMERIC(8,4),  -- ← DPI
    total_value_over_contributions   NUMERIC(8,4),  -- ← TVPI
    enterprise_value                 DECIMAL(18,2), -- ← NAV/Valuation
    quarter_end                      DATE
);

-- Table: underlying_assets  (same as portfolio_companies, investee_companies)
CREATE TABLE underlying_assets (
    asset_id          INT PRIMARY KEY,
    asset_name        NVARCHAR(200),
    gics_sector       NVARCHAR(100),  -- Uses GICS vs free text
    region            NVARCHAR(100),
    acquisition_date  DATE,
    invested_capital  DECIMAL(18,2),  -- ← Invested Capital
    appraised_value   DECIMAL(18,2)   -- ← Fair Market Value
);

-- Sample data
INSERT INTO fund_metrics VALUES
(1, 'CGF-ALPHA-2018', 0.214500, 0.276200, 2.38, 1.10, 2.38, 342000000, '2024-12-31'),
(2, 'CGF-BETA-2020',  0.189300, 0.241800, 1.92, 0.65, 1.92, 218000000, '2024-12-31');

INSERT INTO underlying_assets VALUES
(201, 'Quantum Retail Group',  '25101010', 'Americas',      '2019-04-12', 67000000, 159000000),
(202, 'NovaBio Sciences',      '35202010', 'Europe',        '2020-09-08', 48000000, 112000000),
(203, 'LogiTech Infrastructure','20101010', 'Asia Pacific',  '2021-11-22', 31000000, 48000000);
```

---

### The Core Problem

```
Query: "What is the Net IRR for all Technology sector deals across all clients?"

Platform today: ❌ IMPOSSIBLE
  — Client A: column is `irr_net` in table `fund_performance`
  — Client B: column is `net_irr_pct` in table `portfolio_returns`
  — Client C: column is `internal_rate_return_net` in table `fund_metrics`
  — "Technology" sector: "Software" vs "Technology" vs GICS code "25101010"

With Knowledge Platform: ✅ ONE QUERY, INSTANT ANSWER
  — Canonical metric: NetIRR → maps to all three columns
  — Canonical sector: Technology → maps to "Software", "Technology", GICS 25101010
```

---

## 2. Platform Tenant Architecture

### Tenant Setup

Each fund manager client is a **separate tenant** in the platform. Tenant isolation is strict — Client A cannot see Client B's data.

```
KOP Multi-Tenant Setup:
┌─────────────────────────────────────────────────────┐
│              Knowledge Operating Platform             │
│                                                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────────┐
│  │ Tenant: apex    │  │ Tenant: blueridge│  │ Tenant: citadel  │
│  │                 │  │                  │  │                  │
│  │ PostgreSQL:     │  │ PostgreSQL:       │  │ PostgreSQL:      │
│  │  tenant_apex    │  │  tenant_blueridge │  │  tenant_citadel  │
│  │                 │  │                  │  │                  │
│  │ Qdrant:         │  │ Qdrant:           │  │ Qdrant:          │
│  │  apex_*         │  │  blueridge_*      │  │  citadel_*       │
│  │                 │  │                  │  │                  │
│  │ Graph (Kuzu):   │  │ Graph (Kuzu):     │  │ Graph (Kuzu):    │
│  │  apex.kuzu      │  │  blueridge.kuzu   │  │  citadel.kuzu    │
│  └─────────────────┘  └─────────────────┘  └──────────────────┘
│                                                       │
│  GLOBAL (shared, read-only by all tenants):           │
│  - Private Markets Ontology (OWL)                     │
│  - Platform Taxonomy (GICS, regions)                  │
│  - Platform Glossary (IRR, MOIC, DPI definitions)    │
└─────────────────────────────────────────────────────┘
```

### Tenant Onboarding (Control Plane)

```bash
# Step 1: Create tenant via CLI
kop tenant create \
  --name "apex-capital" \
  --display-name "Apex Capital Partners" \
  --domain "private-markets" \
  --sovereignty-zone US \
  --classification-default CONFIDENTIAL \
  --tier enterprise

# Platform response:
{
  "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
  "tenant_slug": "apex-capital",
  "db_schema": "tenant_apex_capital",
  "storage_bucket": "kop-apex-capital-us-east-1",
  "vector_collection_prefix": "apex_capital",
  "provisioned_at": "2025-05-31T09:00:00Z",
  "status": "active"
}

# Step 2: Assign connector to tenant
kop connector configure sqlserver \
  --tenant apex-capital \
  --host apex-db.internal.corp \
  --database apex_capital_db \
  --user kop_readonly \
  --password "..." \
  --name "apex-main-db"
```

---

## 3. Plane-by-Plane Flow with Sample Data

---

## Plane 1 — Ingestion Plane

**Purpose:** Connect to each client's SQL Server, extract table schemas and row data, push to the platform.

### Connector Configuration (per tenant)

```yaml
# apex-capital SQL Server connector config
connector_id: sqlserver
tenant_id: apex-capital
config:
  host: apex-db.internal.corp
  port: 1433
  database: apex_capital_db
  user: kop_readonly
  schema: dbo
  extraction_mode: schema_and_data
  tables:
    - fund_performance
    - portfolio_companies
    - capital_activity
  incremental_column: reporting_date    # Incremental sync
  full_sync_schedule: "0 2 * * 0"      # Weekly full sync (Sundays 2am)
  incremental_sync_schedule: "0 6 * * *" # Daily incremental (6am)
  row_limit_per_run: 100000
  timeout_seconds: 300
```

### What the Ingestion Connector Does

```
Step 1: Test connection → apex-db.internal.corp:1433 ✓
Step 2: Introspect schema →
  Tables found: fund_performance, portfolio_companies, capital_activity
Step 3: Extract schema DDL (as text asset)
Step 4: Extract data (as JSON rows, batched)
Step 5: Store in S3 (raw zone)
Step 6: Emit DocumentCreatedEvent
```

### Raw Ingestion Output (stored in S3)

```json
// S3 key: s3://kop-apex-capital-us-east-1/raw/sqlserver/apex_capital_db/fund_performance/2025-05-31/batch_001.json

{
  "source_connector": "sqlserver",
  "source_database": "apex_capital_db",
  "source_table": "fund_performance",
  "extracted_at": "2025-05-31T06:02:15Z",
  "row_count": 2,
  "schema": {
    "columns": [
      {"name": "fund_id",        "sql_type": "VARCHAR(20)",   "nullable": false, "is_pk": true},
      {"name": "fund_name",      "sql_type": "VARCHAR(200)",  "nullable": true,  "is_pk": false},
      {"name": "irr_net",        "sql_type": "DECIMAL(8,4)",  "nullable": true,  "is_pk": false},
      {"name": "irr_gross",      "sql_type": "DECIMAL(8,4)",  "nullable": true,  "is_pk": false},
      {"name": "moic",           "sql_type": "DECIMAL(6,2)",  "nullable": true,  "is_pk": false},
      {"name": "dpi",            "sql_type": "DECIMAL(6,2)",  "nullable": true,  "is_pk": false},
      {"name": "tvpi",           "sql_type": "DECIMAL(6,2)",  "nullable": true,  "is_pk": false},
      {"name": "nav_usd",        "sql_type": "BIGINT",        "nullable": true,  "is_pk": false},
      {"name": "reporting_date", "sql_type": "DATE",          "nullable": true,  "is_pk": false}
    ]
  },
  "rows": [
    {"fund_id":"APX-F1","fund_name":"Apex Growth Fund I","irr_net":0.234,"irr_gross":0.289,"moic":2.45,"dpi":1.20,"tvpi":2.45,"nav_usd":485000000,"reporting_date":"2024-12-31"},
    {"fund_id":"APX-F2","fund_name":"Apex Buyout Fund II","irr_net":0.182,"irr_gross":0.241,"moic":1.98,"dpi":0.85,"tvpi":1.98,"nav_usd":312000000,"reporting_date":"2024-12-31"}
  ]
}
```

### Event Emitted

```json
// Redis Stream: kop.ingestion.document.created.v1
{
  "id": "evt-001-apex",
  "type": "kop.ingestion.document.created.v1",
  "source": "/planes/ingestion",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
  "data": {
    "document_id": "doc-apex-fund-perf-20250531",
    "source_connector": "sqlserver",
    "source_uri": "sqlserver://apex-db/apex_capital_db/fund_performance",
    "storage_key": "raw/sqlserver/apex_capital_db/fund_performance/2025-05-31/batch_001.json",
    "content_type": "application/json",
    "asset_type": "database_table",
    "row_count": 2
  }
}
```

**Same process repeats for `blueridge_db` and `citadel_gf_db` under their respective tenants.**

---

## Plane 2 — Metadata Plane

**Purpose:** Automatically harvest technical metadata from each ingested table, compute quality scores, build the asset catalog.

### Metadata Harvester (SQL Schema Harvester)

The platform's SQL Schema Harvester subscribes to `kop.ingestion.document.created.v1` and auto-produces:

```json
// AssetMetadata record stored in PostgreSQL: tenant_apex_capital.asset_metadata

{
  "asset_id": "asset-apex-fund-perf-001",
  "tenant_id": "apex-capital",
  "asset_type": "database_table",

  "technical": {
    "source_system": "SQL Server",
    "source_database": "apex_capital_db",
    "source_table": "fund_performance",
    "format": "relational_table",
    "row_count": 2,
    "column_count": 9,
    "primary_key": ["fund_id"],
    "data_types": {
      "numeric_columns": ["irr_net","irr_gross","moic","dpi","tvpi","nav_usd"],
      "string_columns": ["fund_id","fund_name"],
      "date_columns": ["reporting_date"]
    },
    "value_ranges": {
      "irr_net":   {"min": 0.182, "max": 0.234, "avg": 0.208, "null_pct": 0.0},
      "irr_gross": {"min": 0.241, "max": 0.289, "avg": 0.265, "null_pct": 0.0},
      "moic":      {"min": 1.98,  "max": 2.45,  "avg": 2.215, "null_pct": 0.0},
      "nav_usd":   {"min": 312000000, "max": 485000000,        "null_pct": 0.0}
    },
    "quality_score": 0.91,
    "completeness": 1.0,
    "last_updated": "2024-12-31"
  },

  "business": {
    "name": null,           // ← not yet filled (needs human or AI annotation)
    "description": null,    // ← not yet filled
    "owner": null,
    "domain": "private-markets",
    "tags": ["fund-performance", "irr", "financial-metrics"],   // ← auto-tagged by AI classifier
    "glossary_terms": []    // ← populated after Semantic Plane runs
  },

  "governance": {
    "classification": "CONFIDENTIAL",
    "sovereignty_zone": "US",
    "policy_ids": ["pol-private-markets-default"]
  }
}
```

### Metadata Quality Score Breakdown

```
Quality Score: 0.91 / 1.0

  Completeness:   1.00  (no nulls in key columns)
  Uniqueness:     1.00  (fund_id is unique PK)
  Timeliness:     0.95  (last updated 2024-12-31, within 6 months)
  Consistency:    0.85  (column naming uses abbreviations, not full names)
  Documentation:  0.50  (no business description yet — flagged for steward review)

  → Action Required: Business metadata not filled. Assigned to data steward.
  → Auto-suggestion: "This table likely contains fund performance metrics (IRR, MOIC, DPI, TVPI)."
```

### Parallel: Same Asset Detected in Client B

```json
// AssetMetadata for blueridge: portfolio_returns table
{
  "asset_id": "asset-blueridge-port-returns-001",
  "tenant_id": "blue-ridge",
  "technical": {
    "source_table": "portfolio_returns",
    "column_count": 9,
    "numeric_columns": ["net_irr_pct","gross_irr_pct","return_multiple","distribution_ratio","total_value_ratio","fair_value"],
    "quality_score": 0.88
  }
}
```

> **Note at this point:** The platform does NOT yet know that `apex.fund_performance` and `blueridge.portfolio_returns` represent the same business concept. That resolution happens in the Canonical Plane.

---

## Plane 3 — Canonical Plane

**Purpose:** Resolve that `irr_net`, `net_irr_pct`, and `internal_rate_return_net` all mean **Net IRR**. Create cross-client canonical column and entity mappings.

### Step 1 — Column Fingerprinting

The platform analyzes every numeric column across all tenants:

```
Column Fingerprint Engine:

Candidate A: apex.fund_performance.irr_net
  → range: [0.182, 0.234]
  → type: DECIMAL(8,4)
  → table context: fund_performance
  → column name tokens: ["irr", "net"]
  → embedding similarity to "Internal Rate of Return Net": 0.94

Candidate B: blueridge.portfolio_returns.net_irr_pct
  → range: [0.197, 0.231]
  → type: FLOAT
  → table context: portfolio_returns
  → column name tokens: ["net", "irr", "pct"]
  → embedding similarity to "Internal Rate of Return Net": 0.97

Candidate C: citadel.fund_metrics.internal_rate_return_net
  → range: [0.189, 0.215]
  → type: NUMERIC(10,6)
  → table context: fund_metrics
  → column name tokens: ["internal", "rate", "return", "net"]
  → embedding similarity to "Internal Rate of Return Net": 0.99
```

### Step 2 — Canonical Column Registry

```json
// Canonical column mappings stored in PostgreSQL: canonical_columns

[
  {
    "canonical_id":   "col-canon-net-irr",
    "canonical_name": "NetIRR",
    "display_name":   "Net Internal Rate of Return",
    "description":    "The annualized net return of a fund after management fees and carried interest, expressed as a percentage.",
    "data_type":      "percentage",
    "unit":           "decimal_percentage",
    "domain":         "private-markets.performance",
    "mappings": [
      {
        "tenant_id":    "apex-capital",
        "source_table": "fund_performance",
        "source_column":"irr_net",
        "confidence":   0.97,
        "resolution_method": "embedding_similarity + column_name_tokens"
      },
      {
        "tenant_id":    "blue-ridge",
        "source_table": "portfolio_returns",
        "source_column":"net_irr_pct",
        "confidence":   0.98,
        "resolution_method": "embedding_similarity + column_name_tokens"
      },
      {
        "tenant_id":    "citadel-growth",
        "source_table": "fund_metrics",
        "source_column":"internal_rate_return_net",
        "confidence":   0.99,
        "resolution_method": "exact_semantic_match"
      }
    ]
  },
  {
    "canonical_id":   "col-canon-moic",
    "canonical_name": "MOIC",
    "display_name":   "Multiple on Invested Capital",
    "mappings": [
      {"tenant_id": "apex-capital",   "source_column": "moic",            "confidence": 0.99},
      {"tenant_id": "blue-ridge",     "source_column": "return_multiple",  "confidence": 0.95},
      {"tenant_id": "citadel-growth", "source_column": "money_on_money",   "confidence": 0.93}
    ]
  },
  {
    "canonical_id":   "col-canon-dpi",
    "canonical_name": "DPI",
    "display_name":   "Distributions to Paid-In Capital",
    "mappings": [
      {"tenant_id": "apex-capital",   "source_column": "dpi",                         "confidence": 0.99},
      {"tenant_id": "blue-ridge",     "source_column": "distribution_ratio",           "confidence": 0.94},
      {"tenant_id": "citadel-growth", "source_column": "distributions_over_contributions","confidence": 0.98}
    ]
  },
  {
    "canonical_id":   "col-canon-valuation",
    "canonical_name": "FairMarketValue",
    "display_name":   "Fair Market Value / NAV",
    "mappings": [
      {"tenant_id": "apex-capital",   "source_column": "nav_usd",          "confidence": 0.91},
      {"tenant_id": "blue-ridge",     "source_column": "fair_value",        "confidence": 0.99},
      {"tenant_id": "citadel-growth", "source_column": "enterprise_value",  "confidence": 0.88}
    ]
  }
]
```

### Step 3 — Canonical Entity Mapping (Portfolio Companies)

```json
// The same real company might appear in multiple tenants' data.
// Example: "TechFlow Inc" (Apex) and "DataStream Analytics" (Blue Ridge) are different companies.
// But "Quantum Retail Group" (Citadel) is in GICS sector 25101010 = Consumer Discretionary, not Technology.

// SECTOR CANONICAL MAPPING (critical for cross-client queries!)
{
  "canonical_id":   "sector-canon-technology",
  "canonical_name": "Technology",
  "mappings": [
    {"tenant_id": "apex-capital",   "source_value": "Software",    "table": "portfolio_companies", "column": "sector"},
    {"tenant_id": "blue-ridge",     "source_value": "Technology",  "table": "investee_companies",  "column": "industry_sector"},
    {"tenant_id": "citadel-growth", "source_value": "45101010",    "table": "underlying_assets",   "column": "gics_sector",
     "note": "GICS 45101010 = Internet Software & Services → maps to Technology"}
  ]
}
```

### Canonical Resolution API

```
GET /v1/canonical/resolve?
  column=irr_net&
  source_table=fund_performance&
  tenant_id=apex-capital

Response:
{
  "canonical_id": "col-canon-net-irr",
  "canonical_name": "NetIRR",
  "display_name": "Net Internal Rate of Return",
  "glossary_term_id": "term-net-irr",
  "ontology_uri": "https://spec.edmcouncil.org/fibo/ontology/FBC/FinancialInstruments/FinancialInstruments/NetIRR"
}
```

---

## Plane 4 — Ontology Plane

**Purpose:** Define the formal Private Markets ontology — machine-readable, versioned, and authoritative.

### Private Markets Ontology (OWL 2 / Turtle excerpt)

```turtle
# File: private-markets-ontology-v1.0.ttl

@prefix pm: <https://kop.platform/ontology/private-markets/> .
@prefix fibo: <https://spec.edmcouncil.org/fibo/ontology/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# ── Ontology Declaration ──────────────────────────────
<https://kop.platform/ontology/private-markets/>
    a owl:Ontology ;
    rdfs:label "Private Markets Ontology" ;
    owl:versionInfo "1.0.0" .

# ── Core Classes ──────────────────────────────────────

pm:Fund a owl:Class ;
    rdfs:label "Fund" ;
    rdfs:comment "A pooled investment vehicle managed by a General Partner on behalf of Limited Partners." ;
    rdfs:subClassOf fibo:InvestmentFund .

pm:PortfolioCompany a owl:Class ;
    rdfs:label "Portfolio Company" ;
    rdfs:comment "A company in which a private equity fund has made an investment." .

pm:Deal a owl:Class ;
    rdfs:label "Deal" ;
    rdfs:comment "An investment transaction by a Fund into a Portfolio Company." .

pm:PerformanceMetric a owl:Class ;
    rdfs:label "Performance Metric" ;
    rdfs:comment "A quantitative measure of fund or investment performance." .

pm:NetIRR a owl:Class ;
    rdfs:label "Net Internal Rate of Return" ;
    rdfs:comment "The annualized rate of return after management fees and carried interest." ;
    rdfs:subClassOf pm:PerformanceMetric ;
    rdfs:subClassOf fibo:RateOfReturn .

pm:GrossIRR a owl:Class ;
    rdfs:label "Gross Internal Rate of Return" ;
    rdfs:subClassOf pm:PerformanceMetric .

pm:MOIC a owl:Class ;
    rdfs:label "Multiple on Invested Capital" ;
    rdfs:subClassOf pm:PerformanceMetric .

pm:DPI a owl:Class ;
    rdfs:label "Distributions to Paid-In Capital" ;
    rdfs:subClassOf pm:PerformanceMetric .

pm:TVPI a owl:Class ;
    rdfs:label "Total Value to Paid-In Capital" ;
    rdfs:subClassOf pm:PerformanceMetric .

pm:NAV a owl:Class ;
    rdfs:label "Net Asset Value" ;
    rdfs:subClassOf pm:PerformanceMetric .

pm:FairMarketValue a owl:Class ;
    rdfs:label "Fair Market Value" ;
    rdfs:comment "The estimated market value of a portfolio company as of a reporting date." .

# ── Object Properties ─────────────────────────────────

pm:hasInvestmentIn a owl:ObjectProperty ;
    rdfs:label "has investment in" ;
    rdfs:domain pm:Fund ;
    rdfs:range pm:PortfolioCompany .

pm:hasPerformanceMetric a owl:ObjectProperty ;
    rdfs:domain pm:Fund ;
    rdfs:range pm:PerformanceMetric .

pm:reportedAsOf a owl:ObjectProperty ;
    rdfs:domain pm:PerformanceMetric .

pm:inSector a owl:ObjectProperty ;
    rdfs:domain pm:PortfolioCompany ;
    rdfs:range pm:IndustrySector .

# ── Data Properties ───────────────────────────────────

pm:netIRRValue a owl:DatatypeProperty ;
    rdfs:domain pm:NetIRR ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Stored as decimal fraction: 0.234 = 23.4%" .

pm:moicValue a owl:DatatypeProperty ;
    rdfs:domain pm:MOIC ;
    rdfs:range xsd:decimal .
```

### Ontology Import and Publication

```bash
# Import ontology for the platform (global — applies to all tenants)
kop ontology import private-markets-ontology-v1.0.ttl \
  --format turtle \
  --domain private-markets \
  --global \
  --publish

# Response:
{
  "ontology_id": "ont-pm-v1",
  "uri": "https://kop.platform/ontology/private-markets/",
  "version": "1.0.0",
  "status": "published",
  "class_count": 24,
  "property_count": 31
}
```

---

## Plane 5 — Taxonomy Plane

**Purpose:** Classify portfolio companies and funds into hierarchical categories.

### Private Markets Taxonomy

```json
// Taxonomy: Private Markets Sector Taxonomy
{
  "taxonomy_id": "tax-pm-sector",
  "name": "Private Markets Sector Classification",
  "version": "1.0",
  "is_global": true,
  "nodes": [
    {
      "node_id": "sec-technology",
      "label": "Technology",
      "level": 1,
      "children": [
        {"node_id": "sec-software",       "label": "Software",                "level": 2},
        {"node_id": "sec-internet",       "label": "Internet & Digital",      "level": 2},
        {"node_id": "sec-cybersecurity",  "label": "Cybersecurity",           "level": 2},
        {"node_id": "sec-fintech",        "label": "Financial Technology",    "level": 2}
      ],
      "source_mappings": [
        {"tenant": "apex-capital",   "value": "Software",        "confidence": 0.95},
        {"tenant": "blue-ridge",     "value": "Technology",      "confidence": 0.99},
        {"tenant": "citadel-growth", "value": "45101010",        "confidence": 0.97}
      ]
    },
    {
      "node_id": "sec-healthcare",
      "label": "Healthcare & Life Sciences",
      "level": 1,
      "children": [
        {"node_id": "sec-pharma",      "label": "Pharmaceuticals",        "level": 2},
        {"node_id": "sec-medtech",     "label": "Medical Technology",     "level": 2},
        {"node_id": "sec-biotech",     "label": "Biotechnology",          "level": 2},
        {"node_id": "sec-life-sci",    "label": "Life Sciences Services", "level": 2}
      ],
      "source_mappings": [
        {"tenant": "apex-capital",   "value": "Healthcare",    "confidence": 0.90},
        {"tenant": "blue-ridge",     "value": "Life Sciences", "confidence": 0.88},
        {"tenant": "citadel-growth", "value": "35202010",      "confidence": 0.99}
      ]
    },
    {
      "node_id": "sec-industrials",
      "label": "Industrials",
      "level": 1,
      "source_mappings": [
        {"tenant": "blue-ridge",     "value": "Industrials",  "confidence": 0.99},
        {"tenant": "citadel-growth", "value": "20101010",     "confidence": 0.99}
      ]
    },
    {
      "node_id": "sec-clean-energy",
      "label": "Clean Energy & Sustainability",
      "level": 1,
      "source_mappings": [
        {"tenant": "apex-capital", "value": "Clean Energy", "confidence": 0.99}
      ]
    }
  ]
}
```

---

## Plane 6 — Semantic Plane

**Purpose:** The governed business glossary — authoritative definitions of every financial metric used across all clients.

### Business Glossary Terms

```json
// GlossaryTerms — stored in tenant_global.glossary_terms (platform-wide)

[
  {
    "term_id": "term-net-irr",
    "name": "Net IRR",
    "domain": "private-markets.performance",
    "definition": "The Internal Rate of Return of a private equity fund, calculated net of management fees and carried interest. Expressed as an annualized percentage. The discount rate at which the net present value of all cash flows (capital calls and distributions) equals zero, after deducting all fees.",
    "examples": [
      "Apex Growth Fund I has a Net IRR of 23.4% as of Q4 2024",
      "The fund's net IRR of 19.7% outperformed the benchmark of 18.2%"
    ],
    "synonyms": [
      {"value": "irr_net",                       "type": "deprecated", "source": "apex-capital SQL"},
      {"value": "net_irr_pct",                   "type": "deprecated", "source": "blue-ridge SQL"},
      {"value": "internal_rate_return_net",       "type": "deprecated", "source": "citadel-growth SQL"},
      {"value": "Net Internal Rate of Return",    "type": "preferred"},
      {"value": "Fund Net IRR",                  "type": "acceptable"}
    ],
    "ontology_uri": "https://kop.platform/ontology/private-markets/NetIRR",
    "canonical_column_id": "col-canon-net-irr",
    "status": "published",
    "owner": "risk_analytics_team",
    "approved_by": "chief_data_officer",
    "version": "1.0",
    "effective_date": "2025-01-01"
  },
  {
    "term_id": "term-moic",
    "name": "MOIC",
    "domain": "private-markets.performance",
    "definition": "Multiple on Invested Capital. The ratio of the total value of an investment (realized + unrealized) to the amount of capital originally invested. A MOIC of 2.0x means the investment is worth twice the capital invested.",
    "synonyms": [
      {"value": "moic",             "type": "preferred"},
      {"value": "return_multiple",  "type": "acceptable"},
      {"value": "money_on_money",   "type": "deprecated", "source": "citadel-growth SQL"},
      {"value": "TVPI",             "type": "related",    "note": "TVPI = unrealized MOIC; MOIC sometimes used interchangeably for matured funds"},
      {"value": "Investment Multiple","type": "acceptable"},
      {"value": "Return Multiple",  "type": "acceptable"}
    ],
    "ontology_uri": "https://kop.platform/ontology/private-markets/MOIC",
    "status": "published"
  },
  {
    "term_id": "term-portfolio-company",
    "name": "Portfolio Company",
    "domain": "private-markets.entities",
    "definition": "A company in which a private equity, venture capital, or other alternative investment fund has made an equity or debt investment.",
    "synonyms": [
      {"value": "portfolio_companies", "type": "deprecated", "source": "apex-capital SQL table"},
      {"value": "investee_companies",  "type": "deprecated", "source": "blue-ridge SQL table"},
      {"value": "underlying_assets",   "type": "deprecated", "source": "citadel-growth SQL table"},
      {"value": "Investee",            "type": "acceptable"},
      {"value": "Portfolio Asset",     "type": "acceptable"}
    ],
    "ontology_uri": "https://kop.platform/ontology/private-markets/PortfolioCompany",
    "status": "published"
  }
]
```

---

## Plane 7 — Knowledge Graph Plane

**Purpose:** Build the connected property graph of Funds → Deals → Portfolio Companies → Metrics.

### Graph Construction Pipeline

```
Event received: kop.metadata.asset.harvested.v1
→ Canonical Plane resolves column mappings
→ Knowledge Graph Builder creates nodes and relationships
```

### Nodes Created

```cypher
-- Fund nodes (one per fund per tenant)
CREATE (f:Fund {
  node_id:       "node-apex-fund-1",
  canonical_name: "Apex Growth Fund I",
  source_id:     "APX-F1",
  tenant_id:     "apex-capital",
  vintage_year:  2019,
  strategy:      "Growth Equity"
})

CREATE (f:Fund {
  node_id:       "node-apex-fund-2",
  canonical_name: "Apex Buyout Fund II",
  source_id:     "APX-F2",
  tenant_id:     "apex-capital",
  vintage_year:  2021,
  strategy:      "Buyout"
})

-- Portfolio Company nodes
CREATE (pc:PortfolioCompany {
  node_id:              "node-apex-pc-001",
  canonical_name:       "TechFlow Inc",
  source_id:            "APX-PC-001",
  tenant_id:            "apex-capital",
  sector_canonical:     "Technology",     -- ← canonical (not "Software")
  sector_source:        "Software",       -- ← original
  geography:            "North America",
  entry_date:           "2021-03-15"
})

-- Performance Metric nodes (canonical metric names)
CREATE (m:PerformanceMetric:NetIRR {
  node_id:             "node-apex-f1-net-irr",
  canonical_metric:    "NetIRR",
  source_column:       "irr_net",         -- ← original column name preserved
  value:               0.234,
  value_display:       "23.4%",
  reporting_date:      "2024-12-31",
  tenant_id:           "apex-capital"
})

CREATE (m:PerformanceMetric:MOIC {
  node_id:          "node-apex-f1-moic",
  canonical_metric: "MOIC",
  source_column:    "moic",
  value:            2.45,
  reporting_date:   "2024-12-31",
  tenant_id:        "apex-capital"
})
```

### Relationships Created

```cypher
-- Fund → PortfolioCompany
MATCH (f:Fund {node_id: "node-apex-fund-1"})
MATCH (pc:PortfolioCompany {node_id: "node-apex-pc-001"})
CREATE (f)-[:HAS_INVESTMENT {
  invested_capital:  45000000,
  cost_basis_source: "cost_basis_usd",   -- ← original column
  entry_date:        "2021-03-15"
}]->(pc)

-- Fund → PerformanceMetric
MATCH (f:Fund {node_id: "node-apex-fund-1"})
MATCH (m:NetIRR {node_id: "node-apex-f1-net-irr"})
CREATE (f)-[:HAS_PERFORMANCE_METRIC {as_of: "2024-12-31"}]->(m)

-- PortfolioCompany → Sector (taxonomy node)
MATCH (pc:PortfolioCompany {node_id: "node-apex-pc-001"})
MATCH (s:Sector {node_id: "sec-technology"})
CREATE (pc)-[:IN_SECTOR]->(s)
```

### Resulting Knowledge Graph (visual representation)

```
[Apex Growth Fund I] ──HAS_INVESTMENT──> [TechFlow Inc]
        │                                      │
        │                               IN_SECTOR
        │                                      │
        HAS_PERFORMANCE_METRIC              [Technology]
        │                                      │
    [NetIRR: 23.4%]                    IN_SECTOR (also points to)
    [GrossIRR: 28.9%]             [DataStream Analytics] (blueridge)
    [MOIC: 2.45x]                 [Quantum Retail Group] (citadel)
    [DPI: 1.20x]
    [TVPI: 2.45x]

[BRV Core Fund 2019] ──HAS_INVESTMENT──> [DataStream Analytics]
        │
        HAS_PERFORMANCE_METRIC
        │
    [NetIRR: 19.7%]   ← stored with canonical_metric: "NetIRR"
    [MOIC: 2.12x]       even though source was "net_irr_pct"
```

### Graph Query: Cross-Client "Technology" Portfolio

```cypher
-- Query: All Technology sector investments with NetIRR > 15%
MATCH (f:Fund)-[:HAS_INVESTMENT]->(pc:PortfolioCompany)-[:IN_SECTOR]->(s:Sector)
MATCH (f)-[:HAS_PERFORMANCE_METRIC]->(m:NetIRR)
WHERE s.node_id = 'sec-technology'
  AND m.value > 0.15
RETURN
  f.canonical_name AS fund,
  pc.canonical_name AS company,
  m.value AS net_irr,
  m.reporting_date AS as_of,
  f.tenant_id AS client

-- Result:
┌────────────────────────┬──────────────────────┬─────────┬────────────┬──────────────┐
│ fund                   │ company              │ net_irr │ as_of      │ client       │
├────────────────────────┼──────────────────────┼─────────┼────────────┼──────────────┤
│ Apex Growth Fund I     │ TechFlow Inc          │  0.234  │ 2024-12-31 │ apex-capital │
│ BRV Growth Fund 2021   │ DataStream Analytics  │  0.231  │ 2024-12-31 │ blue-ridge   │
└────────────────────────┴──────────────────────┴─────────┴────────────┴──────────────┘

-- This query was IMPOSSIBLE before the Knowledge Platform.
-- Source columns were: irr_net (Apex), net_irr_pct (Blue Ridge)
-- Sectors were: "Software" (Apex), "Technology" (Blue Ridge)
```

---

## Plane 8 — Vector Plane

**Purpose:** Create semantic embeddings of all knowledge assets for AI-powered retrieval.

### What Gets Embedded

```
Embedded content per asset type:

1. Table + Column Descriptions (schema-level):
   Text: "fund_performance table in apex_capital_db containing columns:
          irr_net (Net Internal Rate of Return after fees),
          irr_gross (Gross IRR before fees), moic (Multiple on Invested Capital),
          dpi (Distributions to Paid-In), tvpi (Total Value to Paid-In),
          nav_usd (Net Asset Value in USD)"
   → Vector stored in collection: apex_capital_schema_text3large

2. Data Row Embeddings (for semantic row-level search):
   Text: "Apex Growth Fund I performance: Net IRR 23.4%, Gross IRR 28.9%,
          MOIC 2.45x, DPI 1.20x, TVPI 2.45x, NAV $485M as of Q4 2024"
   → Vector stored in collection: apex_capital_fund_data_text3large

3. Portfolio Company Embeddings:
   Text: "TechFlow Inc - Software company in North America.
          Invested April 2021 at $45M cost basis.
          Current valuation $112M. 2.49x gross return."
   → Vector stored in collection: apex_capital_companies_text3large

4. Glossary Term Embeddings:
   Text: "Net IRR: The Internal Rate of Return net of management fees
          and carried interest. Also known as irr_net, net_irr_pct,
          internal_rate_return_net. Domain: private-markets.performance."
   → Vector stored in collection: global_glossary_text3large
```

### Embedding Registry Entry

```json
{
  "model_id": "emb-openai-text3large-v1",
  "name": "text-embedding-3-large",
  "version": "2024-02",
  "provider": "openai",
  "dimensions": 3072,
  "max_tokens": 8191,
  "is_active": true,
  "collections": [
    "apex_capital_schema_text3large",
    "apex_capital_fund_data_text3large",
    "apex_capital_companies_text3large",
    "blueridge_schema_text3large",
    "blueridge_fund_data_text3large",
    "citadel_schema_text3large",
    "citadel_fund_data_text3large",
    "global_glossary_text3large"
  ]
}
```

### Qdrant Collection Sample

```json
// Qdrant collection: apex_capital_fund_data_text3large
// Point (vector record) for Apex Growth Fund I

{
  "id": "vec-apex-f1-perf-20241231",
  "vector": [0.0234, -0.1892, 0.4521, ...],  // 3072-dimensional
  "payload": {
    "tenant_id":        "apex-capital",
    "asset_id":         "asset-apex-fund-perf-001",
    "source_table":     "fund_performance",
    "source_row_id":    "APX-F1",
    "canonical_type":   "FundPerformance",
    "fund_name":        "Apex Growth Fund I",
    "reporting_date":   "2024-12-31",
    "canonical_metrics": {
      "NetIRR":  0.234,
      "MOIC":    2.45,
      "DPI":     1.20,
      "TVPI":    2.45,
      "NAV_USD": 485000000
    },
    "embedding_model_id": "emb-openai-text3large-v1",
    "embedded_at":        "2025-05-31T06:15:00Z"
  }
}
```

---

## Plane 9 — Search Plane

**Purpose:** Enable unified search across all knowledge assets using keyword, semantic, and hybrid strategies.

### OpenSearch Index Structure

```json
// OpenSearch index: apex_capital_knowledge_assets
// Index mapping
{
  "mappings": {
    "properties": {
      "tenant_id":          {"type": "keyword"},
      "asset_type":         {"type": "keyword"},
      "canonical_name":     {"type": "text", "analyzer": "english"},
      "description":        {"type": "text", "analyzer": "english"},
      "canonical_metrics":  {"type": "object"},
      "sector_canonical":   {"type": "keyword"},
      "domain":             {"type": "keyword"},
      "reporting_date":     {"type": "date"},
      "glossary_terms":     {"type": "keyword"},
      "embedding":          {"type": "knn_vector", "dimension": 3072}
    }
  }
}
```

### Search Query 1: Semantic Search (user types natural language)

```
User query: "Which of our portfolio companies in healthcare have the best returns?"

Search flow:
1. Embed query → [0.0891, -0.2341, ...]
2. Semantic search in Qdrant (apex_capital_companies collection)
3. Keyword boost for "healthcare" → taxonomy node sec-healthcare
4. RRF fusion of semantic + keyword results

Result:
┌───────────────────┬───────────────┬────────────┬───────────┐
│ company           │ sector        │ current val│ return    │
├───────────────────┼───────────────┼────────────┼───────────┤
│ MedCore Solutions │ Healthcare    │ $98M       │ 1.58x     │
│ PharmaLink Corp   │ Life Sciences │ $87M       │ 1.58x     │  ← from blue-ridge
│ NovaBio Sciences  │ Biotechnology │ $112M      │ 2.33x     │  ← from citadel
└───────────────────┴───────────────┴────────────┴───────────┘

Note: "Life Sciences" and "Biotechnology" resolved to sec-healthcare taxonomy node.
```

### Search Query 2: Metric-Filtered Search

```
User query: "Funds with Net IRR above 20%"

Platform translates:
  "Net IRR" → canonical_metric: NetIRR  (via glossary term resolution)
  "above 20%" → filter: canonical_metrics.NetIRR > 0.20

Search:
  GET /v1/search
  {
    "query": "Funds with Net IRR above 20%",
    "strategies": ["semantic", "metadata"],
    "filters": {
      "asset_type": "FundPerformance",
      "canonical_metrics.NetIRR": {"gt": 0.20}
    }
  }

Result:
┌──────────────────────────┬─────────┬────────────────────┐
│ fund                     │ net_irr │ source_column      │
├──────────────────────────┼─────────┼────────────────────┤
│ Apex Growth Fund I       │ 23.4%   │ irr_net            │
│ BRV Growth Fund 2021     │ 23.1%   │ net_irr_pct        │
│ CGF-ALPHA-2018           │ 21.5%   │ internal_rate_return_net │
└──────────────────────────┴─────────┴────────────────────┘
```

---

## Plane 10 — Governance Plane

**Purpose:** Ensure only authorized users see the right data, with the right classification controls.

### Role Setup (per tenant)

```yaml
# Roles configured for Apex Capital tenant
roles:
  - role: apex_fund_manager
    tenant: apex-capital
    permissions:
      - "read:all_assets"
      - "write:annotations"
      - "read:performance_metrics"
    asset_access:
      classification: [INTERNAL, CONFIDENTIAL]

  - role: apex_lp_viewer
    tenant: apex-capital
    permissions:
      - "read:fund_performance"
    asset_access:
      classification: [INTERNAL]
      funds: ["APX-F1"]           # LP can only see their own fund

  - role: apex_data_steward
    tenant: apex-capital
    permissions:
      - "read:all_assets"
      - "write:metadata"
      - "approve:glossary_terms"
      - "classify:assets"
```

### Authorization Decision (every API call)

```
Request: GET /v1/search?query=IRR&tenant=apex-capital
Auth Token: user: john.smith@apex.com, role: apex_lp_viewer, fund: APX-F1

Authorization flow:
Layer 1 — Tenant Isolation: tenant_id=apex-capital ✓ (cannot see blue-ridge data)
Layer 2 — RBAC: apex_lp_viewer → has "read:fund_performance" ✓
Layer 3 — ABAC: fund_access = ["APX-F1"] → filter results to APX-F1 only
Layer 4 — Classification: max_classification = INTERNAL → exclude CONFIDENTIAL

Decision: ALLOW (with filter: fund_id = APX-F1)

Result returned:
  [Apex Growth Fund I performance — APX-F1 only] ✓

NOT returned:
  [Apex Buyout Fund II — APX-F2] ✗ (ABAC: different fund)
  [Blue Ridge data] ✗ (tenant isolation)
  [Citadel data] ✗ (tenant isolation)
```

### Data Sovereignty Enforcement

```
Apex Capital declared sovereignty_zone: US

When a query arrives:
  → Postgres queries run against tenant_apex_capital schema in US-East RDS ✓
  → Vector queries run against Qdrant cluster in us-east-1 ✓
  → No data written to or read from EU infrastructure ✓

If citadel-growth declared sovereignty_zone: EU:
  → Postgres in EU-West RDS
  → Qdrant cluster in eu-west-1
  → KOP routing layer enforces this at storage adapter level
```

---

## Plane 11 — Lineage Plane

**Purpose:** Track the complete provenance chain from raw SQL table to AI answer.

### Lineage Events Captured

```
Raw SQL Row (apex.fund_performance, row APX-F1)
    ↓ [ingestion.created] by: sqlserver-connector
S3 Raw JSON (s3://kop-apex-capital-us-east-1/raw/fund_performance/batch_001.json)
    ↓ [metadata.harvested] by: sql-schema-harvester
AssetMetadata Record (asset-apex-fund-perf-001)
    ↓ [canonical.mapped] by: column-fingerprint-engine
CanonicalColumnMapping (col-canon-net-irr → irr_net)
    ↓ [knowledge_graph.node.created] by: graph-builder
Graph Node (node-apex-f1-net-irr, NetIRR: 0.234)
    ↓ [vector.embedding.created] by: openai-embedding-pipeline
Vector Point (vec-apex-f1-perf-20241231)
    ↓ [search.indexed] by: opensearch-indexer
OpenSearch Document (apex_capital_knowledge_assets/APX-F1)
    ↓ [ai.retrieval.executed] by: rag-pipeline
RAG Context Item (retrieved for query: "IRR for Apex funds")
    ↓ [ai.response.generated] by: llm-claude-3
AI Response ("Apex Growth Fund I has a Net IRR of 23.4%...")
```

### Lineage API Response

```json
GET /v1/lineage/node-apex-f1-net-irr/upstream

{
  "asset_id": "node-apex-f1-net-irr",
  "asset_name": "NetIRR metric for Apex Growth Fund I",
  "upstream_chain": [
    {
      "step": 1,
      "asset_id": "asset-apex-fund-perf-001",
      "asset_type": "AssetMetadata",
      "transformation": "sql_schema_harvesting",
      "actor": "sql-schema-harvester-v1",
      "timestamp": "2025-05-31T06:05:00Z"
    },
    {
      "step": 2,
      "asset_id": "doc-apex-fund-perf-20250531",
      "asset_type": "RawIngestionDocument",
      "transformation": "sqlserver_connector_extraction",
      "actor": "sqlserver-connector-v1",
      "source_uri": "sqlserver://apex-db/apex_capital_db/fund_performance/APX-F1",
      "timestamp": "2025-05-31T06:02:15Z"
    }
  ],
  "source_of_truth": {
    "system":   "SQL Server",
    "host":     "apex-db.internal.corp",
    "database": "apex_capital_db",
    "table":    "fund_performance",
    "column":   "irr_net",
    "row_id":   "APX-F1",
    "value":    0.234
  }
}
```

---

## Plane 12 — Observability Plane

**Purpose:** Monitor platform health, data freshness, and ingestion quality in real time.

### Key Platform Metrics (Prometheus)

```
# Ingestion metrics
kop_ingestion_total{tenant="apex-capital", connector="sqlserver"} 847
kop_ingestion_failed_total{tenant="apex-capital"} 3
kop_ingestion_latency_seconds_p99{tenant="apex-capital"} 4.2

# Canonical resolution metrics
kop_canonical_resolution_total{tenant="apex-capital", method="embedding"} 156
kop_canonical_resolution_confidence{tenant="apex-capital", column="irr_net"} 0.97
kop_canonical_unresolved_total{tenant="apex-capital"} 4

# Search metrics
kop_search_latency_seconds_p99{tenant="apex-capital", strategy="hybrid"} 0.187
kop_search_requests_total{tenant="apex-capital"} 2341

# Graph metrics
kop_graph_nodes_total{tenant="apex-capital", node_type="Fund"} 2
kop_graph_nodes_total{tenant="apex-capital", node_type="PortfolioCompany"} 3
kop_graph_nodes_total{tenant="apex-capital", node_type="PerformanceMetric"} 12
kop_graph_relationships_total{tenant="apex-capital"} 18

# Data freshness
kop_asset_freshness_days{tenant="apex-capital", asset_type="FundPerformance"} 151
  # ← This is Q4 2024 data. Alert fires if > 100 days since reporting_date
```

### Alert Example

```yaml
# Grafana alert rule
- name: stale_fund_performance_data
  condition: kop_asset_freshness_days{asset_type="FundPerformance"} > 100
  message: "Fund performance data is stale for tenant {{ $labels.tenant }}.
            Last reporting date is more than 100 days old.
            This may indicate a broken SQL Server connector or missed sync."
  severity: warning
  notify: [data_ops_slack, tenant_admin_email]
```

---

## Plane 13 — AI Consumption Plane

**Purpose:** Power natural language queries over the multi-tenant knowledge platform using governed RAG.

### RAG Pipeline for Private Markets Query

```
Query: "What is the IRR and MOIC for all technology deals across all our clients?"

Step 1 — Query Analysis
  Intent: performance_metric_lookup
  Entities detected: ["IRR", "MOIC", "technology"]
  Canonical resolution:
    "IRR"        → canonical_metric: NetIRR (via glossary term-net-irr)
    "MOIC"       → canonical_metric: MOIC
    "technology" → sector: sec-technology (via taxonomy)
  Authorized tenants: [apex-capital, blue-ridge, citadel-growth]
    (user has cross-tenant analyst role)

Step 2 — Multi-Modal Retrieval (parallel)

  [Vector Search]
    Query embedding → top-10 similar fund data points
    Filter: sector_canonical = "Technology"
    → Returns: TechFlow (Apex), DataStream Analytics (Blue Ridge)

  [Graph Search]
    MATCH (f:Fund)-[:HAS_INVESTMENT]->(pc:PortfolioCompany)
    MATCH (pc)-[:IN_SECTOR]->(s:Sector {node_id:"sec-technology"})
    MATCH (f)-[:HAS_PERFORMANCE_METRIC]->(m:PerformanceMetric)
    WHERE m.canonical_metric IN ["NetIRR", "MOIC"]
    → Returns: 4 fund-company-metric triples

  [Metadata Search]
    Filter: canonical_metrics.NetIRR exists AND sector_canonical = Technology
    → Returns: 3 asset records with full metadata

Step 3 — Reranking
  RRF fusion of vector + graph + metadata results
  Top results after reranking: 3 fund performance records

Step 4 — Context Assembly
  Structured context (NOT raw text chunks):

  {
    "context_type": "structured_entities",
    "items": [
      {
        "entity_type": "FundInvestment",
        "fund": "Apex Growth Fund I",
        "company": "TechFlow Inc",
        "sector": "Technology",
        "metrics": {"NetIRR": "23.4%", "MOIC": "2.45x"},
        "as_of": "2024-12-31",
        "source": "apex-capital / fund_performance.irr_net"
      },
      {
        "entity_type": "FundInvestment",
        "fund": "BRV Growth Fund 2021",
        "company": "DataStream Analytics",
        "sector": "Technology",
        "metrics": {"NetIRR": "23.1%", "MOIC": "1.75x"},
        "as_of": "2024-12-31",
        "source": "blue-ridge / portfolio_returns.net_irr_pct"
      }
    ],
    "token_count": 412,
    "citations": [
      {"asset_id": "asset-apex-fund-perf-001", "source_column": "irr_net"},
      {"asset_id": "asset-blueridge-port-returns-001", "source_column": "net_irr_pct"}
    ]
  }

Step 5 — Governance Filter
  User has access to apex-capital ✓
  User has access to blue-ridge ✓
  Classification of results: CONFIDENTIAL — user has CONFIDENTIAL clearance ✓

Step 6 — LLM Call (Claude / GPT-4)
  System prompt with structured context injected
  → Model generates response grounded in platform data

Step 7 — Lineage Recording
  kop.ai.retrieval.executed.v1 emitted
  Which knowledge assets grounded this response: logged
```

### AI Response

```
Query: "What is the IRR and MOIC for all technology deals across all our clients?"

Answer (generated by LLM, grounded in KOP):

Based on Q4 2024 data, here are your technology sector investments:

| Client              | Fund                   | Company              | Net IRR | MOIC  | As Of       |
|---------------------|------------------------|----------------------|---------|-------|-------------|
| Apex Capital        | Apex Growth Fund I     | TechFlow Inc         | 23.4%   | 2.45x | Dec 31 2024 |
| Blue Ridge Ventures | BRV Growth Fund 2021   | DataStream Analytics | 23.1%   | 1.75x | Dec 31 2024 |

Key observations:
• Both technology investments are performing above 20% Net IRR, exceeding typical PE benchmarks of 18%.
• TechFlow Inc has a stronger MOIC (2.45x vs 1.75x), though both funds are relatively young.
• BRV Growth Fund 2021 has a higher current valuation ($195M NAV) vs Apex Growth Fund I's $485M total NAV
  — note Apex has a larger, diversified fund with multiple holdings.

Sources: apex_capital_db.fund_performance.irr_net, blueridge_db.portfolio_returns.net_irr_pct
All figures are as-of reported values. Net IRR is after management fees and carried interest.
```

---

## Plane 14 — Agent Consumption Plane

**Purpose:** Expose the platform as governed MCP tools so AI agents (Claude, etc.) can query portfolio knowledge autonomously.

### MCP Server Configuration

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "portfolio-knowledge": {
      "command": "kop-mcp",
      "args": ["--tenant", "apex-capital", "--port", "8080"],
      "env": {
        "KOP_API_URL": "https://kop.internal.corp",
        "KOP_TOKEN":   "eyJ..."
      }
    }
  }
}
```

### Available MCP Tools (Private Markets Edition)

```json
[
  {
    "name": "kop_get_fund_performance",
    "description": "Retrieve fund performance metrics (Net IRR, MOIC, DPI, TVPI, NAV) for one or more funds. Use this when asked about fund returns, IRR, multiples, or performance.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "fund_name":       {"type": "string", "description": "Fund name or partial name"},
        "metric":          {"type": "string", "enum": ["NetIRR","GrossIRR","MOIC","DPI","TVPI","NAV"], "description": "Canonical metric name"},
        "as_of_date":      {"type": "string", "format": "date"},
        "min_value":       {"type": "number"},
        "max_value":       {"type": "number"}
      }
    }
  },
  {
    "name": "kop_get_portfolio_companies",
    "description": "Search portfolio companies by name, sector, geography, or return profile.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "sector":          {"type": "string", "description": "Canonical sector name (e.g., Technology, Healthcare)"},
        "geography":       {"type": "string"},
        "min_return_moic": {"type": "number"},
        "entry_year":      {"type": "integer"}
      }
    }
  },
  {
    "name": "kop_define_metric",
    "description": "Get the official definition of a financial metric. Use when you need to clarify what IRR, MOIC, DPI, TVPI, or other metrics mean.",
    "inputSchema": {
      "type": "object",
      "required": ["metric_name"],
      "properties": {
        "metric_name": {"type": "string", "description": "The metric name (e.g., IRR, MOIC, DPI, net irr, return multiple)"}
      }
    }
  },
  {
    "name": "kop_compare_funds",
    "description": "Compare two or more funds side by side on performance metrics.",
    "inputSchema": {
      "type": "object",
      "required": ["fund_names"],
      "properties": {
        "fund_names": {"type": "array", "items": {"type": "string"}},
        "metrics":    {"type": "array", "items": {"type": "string"}}
      }
    }
  },
  {
    "name": "kop_get_lineage",
    "description": "Get the data lineage for a specific metric or asset — where did this number come from?",
    "inputSchema": {
      "type": "object",
      "required": ["asset_name"],
      "properties": {
        "asset_name": {"type": "string"}
      }
    }
  }
]
```

### Agent Conversation Example

```
User → Claude: "Compare the Net IRR of Apex Growth Fund I vs BRV Growth Fund 2021,
                and tell me where the 'return_multiple' column in Blue Ridge maps to."

Claude calls: kop_compare_funds
  {
    "fund_names": ["Apex Growth Fund I", "BRV Growth Fund 2021"],
    "metrics": ["NetIRR", "MOIC", "DPI"]
  }

Tool returns:
  {
    "comparison": [
      {
        "fund": "Apex Growth Fund I",
        "tenant": "apex-capital",
        "NetIRR": {"value": 0.234, "source_column": "irr_net"},
        "MOIC":   {"value": 2.45,  "source_column": "moic"},
        "DPI":    {"value": 1.20,  "source_column": "dpi"}
      },
      {
        "fund": "BRV Growth Fund 2021",
        "tenant": "blue-ridge",
        "NetIRR": {"value": 0.231, "source_column": "net_irr_pct"},
        "MOIC":   {"value": 1.75,  "source_column": "return_multiple"},
        "DPI":    {"value": 0.30,  "source_column": "distribution_ratio"}
      }
    ]
  }

Claude calls: kop_define_metric
  {"metric_name": "return_multiple"}

Tool returns:
  {
    "canonical_name": "MOIC",
    "display_name": "Multiple on Invested Capital",
    "definition": "The ratio of total value (realized + unrealized) to invested capital.",
    "synonyms_found": ["return_multiple", "moic", "money_on_money"],
    "source": "Blue Ridge uses 'return_multiple' — this is the same as MOIC."
  }

Claude → User:
"Here's the comparison:

| Metric  | Apex Growth Fund I | BRV Growth Fund 2021 |
|---------|--------------------|----------------------|
| Net IRR | 23.4%              | 23.1%                |
| MOIC    | 2.45x              | 1.75x                |
| DPI     | 1.20x              | 0.30x                |

Both funds have very similar Net IRR (~23%), but Apex Growth Fund I has
a significantly higher MOIC (2.45x vs 1.75x) and has already distributed
1.20x back to investors (DPI), while BRV Growth Fund 2021 is still in
its early hold period with minimal distributions (0.30x DPI).

Regarding Blue Ridge's 'return_multiple' column: the Knowledge Platform
has confirmed this is exactly the same metric as MOIC (Multiple on Invested
Capital). Blue Ridge uses a different column name in their SQL database,
but the platform's Canonical Plane resolves this automatically."
```

---

## 4. End-to-End Query Walkthrough

### Query: "What is the IRR for Apex Growth Fund I?"

```
                        FULL PLATFORM FLOW
                        ──────────────────

User/Agent Request
        │
        ▼
[17] API Plane
  ├─ Auth: validate JWT → extract tenant_id=apex-capital
  ├─ Rate limit: 1000 req/min → within limit ✓
  └─ Route → AI Consumption Plane
        │
        ▼
[14] AI Consumption Plane — RAG Pipeline
  ├─ Query analysis: "IRR" → canonical: NetIRR, GrossIRR
  ├─ Entity: "Apex Growth Fund I" → entity resolution → node-apex-fund-1
  └─ Dispatch retrieval (parallel):
        │
        ├──── [09] Vector Plane ─────────────────────────────────┐
        │       Query Qdrant: apex_capital_fund_data_text3large   │
        │       Filter: source_row_id = APX-F1                    │
        │       → Returns: vec-apex-f1-perf-20241231             │
        │       Score: 0.94                                       │
        │                                                         │
        ├──── [08] Knowledge Graph Plane ───────────────────────── │
        │       Kuzu query:                                        │
        │       MATCH (f:Fund {node_id:"node-apex-fund-1"})       │
        │       MATCH (f)-[:HAS_PERFORMANCE_METRIC]->(m:NetIRR)   │
        │       RETURN m.value, m.reporting_date                   │
        │       → Returns: {value: 0.234, date: "2024-12-31"}     │
        │                                                         │
        └──── [10] Search Plane ─────────────────────────────────┘
                OpenSearch query:
                fund_name: "Apex Growth Fund I"
                + canonical_metrics exists
                → Returns: full metadata record

  ├─ RRF Fusion: merge 3 retrieval results → top result confirmed
  │
  ├─ [11] Governance Plane
  │     Authorization: user has read:fund_performance ✓
  │     Classification: CONFIDENTIAL — user has clearance ✓
  │     Fund access: APX-F1 in user's fund_access list ✓
  │     Decision: ALLOW
  │
  ├─ Context Assembly:
  │     "Apex Growth Fund I NetIRR 23.4% as of 2024-12-31.
  │      Source: apex_capital_db.fund_performance.irr_net"
  │
  ├─ LLM Call with context
  │
  ├─ [12] Lineage Plane
  │     Record: kop.ai.retrieval.executed.v1
  │     Assets cited: [asset-apex-fund-perf-001]
  │     Query: "What is the IRR for Apex Growth Fund I?"
  │     Actor: user@apex.com
  │
  └─ [13] Observability Plane
        kop_rag_retrieval_latency_seconds = 0.142s
        kop_search_requests_total++ (apex-capital)

        ▼
Response returned:
  "Apex Growth Fund I has a Net IRR of 23.4% (gross: 28.9%) as of Q4 2024.
   Source: apex_capital_db, table: fund_performance, column: irr_net."
```

---

## 5. What This Unlocks

### Before the Knowledge Platform

| Capability | Status |
|-----------|--------|
| Query "Net IRR" across all clients | ❌ Impossible — different column names |
| Compare "Technology" sector across clients | ❌ Impossible — different sector taxonomies |
| Ask "which fund has the best MOIC?" | ❌ Impossible — MOIC called return_multiple in Blue Ridge |
| Understand what a column means | ❌ No metadata, no definitions |
| Trace where a number came from | ❌ No lineage |
| AI chat over portfolio data | ❌ LLM hallucinates without grounding |
| Control who sees which fund's data | ❌ Managed at application layer only |

### After the Knowledge Platform

| Capability | Status |
|-----------|--------|
| Query any canonical metric across all clients | ✅ Canonical Plane resolves naming |
| Unified sector/taxonomy search | ✅ Taxonomy Plane normalizes sectors |
| AI-powered portfolio Q&A | ✅ RAG grounded in canonical knowledge graph |
| "Where did this number come from?" | ✅ Full lineage from SQL row to AI response |
| Agent tools for portfolio analysts | ✅ MCP tools with governed data access |
| Investor-level access control | ✅ RBAC + ABAC, fund-level scoping |
| Cross-client benchmarking (same tenant group) | ✅ Cross-tenant graph queries (permissioned) |
| New client onboarded in < 1 day | ✅ SQL connector + canonical mapping = live |
| Regulatory audit trail | ✅ Lineage plane + governance log |
```
