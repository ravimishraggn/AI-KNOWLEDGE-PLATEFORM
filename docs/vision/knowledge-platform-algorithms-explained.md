# Knowledge Platform — Algorithms, Design Decisions, and Concepts Explained
## Four Questions Answered in Plain Language

> This document answers four architectural questions raised during the private markets use case review.
> Every explanation uses the same example: three fund managers with `irr_net`, `net_irr_pct`, and `internal_rate_return_net` all meaning "Net IRR".

---

## Question 1 — Canonical Mapping: How Does the Platform Know That Three Different Column Names Mean the Same Thing?

### The Core Challenge

You have three SQL Server databases. Nobody told the platform anything. It must figure out — on its own — that:

```
apex.fund_performance.irr_net           = "Net IRR"
blueridge.portfolio_returns.net_irr_pct = "Net IRR"  
citadel.fund_metrics.internal_rate_return_net = "Net IRR"
```

There is no single algorithm that solves this. The platform uses **six signals in combination**, then computes a weighted confidence score. Here is each signal explained simply.

---

### Signal 1 — Token Decomposition and Keyword Matching

**What it does:** Break the column name into words and match against a known dictionary of financial terms.

```
Column: irr_net
  Split on underscore/camelCase:    ["irr", "net"]
  Expand known abbreviations:       "irr" → "internal_rate_of_return"
  Identify qualifiers:              "net" → net (after fees)
  Known metric match:               "internal_rate_of_return" + "net" → NetIRR
  Signal confidence:                0.91

Column: net_irr_pct
  Tokens:                           ["net", "irr", "pct"]
  Expand:                           "pct" → percentage, "irr" → internal_rate_of_return
  Qualifier first:                  "net" + "internal_rate_of_return" → NetIRR
  "pct" confirms it is a percentage metric (decimal or percentage-expressed)
  Signal confidence:                0.95

Column: internal_rate_return_net
  Tokens:                           ["internal", "rate", "return", "net"]
  No abbreviation needed — this IS the full name
  "net" qualifier at end
  Signal confidence:                0.99
```

**The abbreviation dictionary is domain-specific.** For private markets you pre-load:
```python
ABBREVIATIONS = {
  "irr":  "internal_rate_of_return",
  "moic": "multiple_on_invested_capital",
  "dpi":  "distributions_to_paid_in",
  "tvpi": "total_value_to_paid_in",
  "nav":  "net_asset_value",
  "ltm":  "last_twelve_months",
  "ytd":  "year_to_date",
  "fmv":  "fair_market_value",
  "lp":   "limited_partner",
  "gp":   "general_partner",
  "pct":  "percentage",
  "usd":  "us_dollar",
  "amt":  "amount",
}

QUALIFIERS = {
  "net":   "after_fees",
  "gross": "before_fees",
  "ttm":   "trailing_twelve_months",
  "cum":   "cumulative",
  "adj":   "adjusted",
}
```

Every industry (banking, healthcare, insurance) gets its own dictionary. Teams extend it.

---

### Signal 2 — Value Range Plausibility

**What it does:** Look at the actual data values. Does the number range make sense for the claimed metric?

```
Column: irr_net → values: [0.182, 0.234]
  Range: 0.0 to 1.0 → plausible as decimal percentage
  Typical IRR range: 0.05 to 0.50 → ✓ fits
  Not plausible as: dollar amount, row count, boolean, ID
  Signal confirms: this is a rate/percentage metric

Column: moic → values: [1.98, 2.45]
  Range: 1.0 to 10.0 → plausible as a multiple (returns)
  Not plausible as: IRR (would be > 100%), NAV (too small for dollar amount)
  Signal confirms: this is a return multiple metric

Counter-example (why this matters):
  Column: fund_id → values: ["APX-F1", "APX-F2"]
  Even if someone named a column "irr_fund_id", the string values rule out
  any mapping to a numeric financial metric.
```

**Value statistics captured:**
```
{
  min:       0.182,
  max:       0.234,
  mean:      0.208,
  std_dev:   0.026,
  null_pct:  0.0,
  data_type: "DECIMAL",
  is_pct_range: true,    // all values between -1 and 1
  is_multiple_range: false,
  is_currency: false
}
```

---

### Signal 3 — Column Co-occurrence Context

**What it does:** Look at what other columns exist in the same table. If a column sits next to known metric columns, the whole table is "fund performance" and that context raises confidence on every column in it.

```
Table: fund_performance
  Columns: fund_id, fund_name, irr_net, irr_gross, moic, dpi, tvpi, nav_usd, reporting_date

  irr_gross already matched to "Gross IRR" with 0.95 confidence
  moic already matched to "MOIC" with 0.99 confidence
  dpi already matched to "DPI" with 0.98 confidence

  → Table context = "FundPerformance" (high confidence)
  → irr_net co-occurs with irr_gross → net vs gross pair → NetIRR boosted to 0.97

Table: portfolio_returns
  Columns: net_irr_pct, gross_irr_pct, return_multiple, distribution_ratio, total_value_ratio, fair_value

  gross_irr_pct matched to "GrossIRR" → confirms net_irr_pct = "NetIRR" (net/gross pair)
  return_multiple co-occurs with distribution_ratio → MOIC / DPI pattern
  → Same FundPerformance pattern confirmed for this table
```

This is called **structural pattern matching** — the pattern of columns in a table tells you the table's purpose, which in turn tells you what each column means.

---

### Signal 4 — Semantic Embedding Similarity

**What it does:** Convert the column context into a vector and compare it to a library of pre-built canonical metric vectors. Closest match wins.

```
Input text constructed per column:
  "Column: irr_net | Table: fund_performance | Type: DECIMAL(8,4) |
   Co-occurring with: irr_gross, moic, dpi, tvpi, nav_usd |
   Value range: 0.18 to 0.29 | Context: fund performance data"

Embed this → 3072-dimensional vector

Compare against pre-built canonical metric embeddings:
  "NetIRR: Net Internal Rate of Return, fund return after fees" → similarity: 0.94
  "GrossIRR: Gross Internal Rate of Return, before fees"       → similarity: 0.71
  "MOIC: Multiple on Invested Capital"                         → similarity: 0.32
  "DPI: Distributions to Paid-In Capital"                     → similarity: 0.28

→ Closest: NetIRR at 0.94. Signal confidence: 0.94
```

The canonical metric embeddings are **pre-built by the platform team** using expert-written definitions. This is the "seed knowledge" that makes the system work.

---

### Signal 5 — Fuzzy String Matching

**What it does:** Direct string distance comparison between the column name and all canonical metric names.

```
Metrics compared: Levenshtein distance, Jaro-Winkler similarity, n-gram overlap

irr_net vs "NetIRR":
  After normalization (remove underscores, lowercase, expand abbreviations):
    "irrnet" vs "netirr"
  Jaro-Winkler: 0.78
  After token-level comparison ["irr","net"] vs ["net","irr"]: perfect set match
  Signal confidence: 0.85

net_irr_pct vs "NetIRR":
  Normalized: "netirr" vs "netirr"
  After dropping "pct" suffix (known unit token)
  Exact match confidence: 0.95

internal_rate_return_net vs "Net Internal Rate of Return":
  Token overlap: ["internal","rate","return","net"] vs ["net","internal","rate","of","return"]
  Jaccard similarity: 4/5 = 0.80
  After reordering: same token set → high confidence
  Signal confidence: 0.90
```

---

### Signal 6 — LLM-Assisted Classification (for ambiguous cases only)

**What it does:** For columns where signals 1-5 produce a confidence below 0.75, the platform sends the column context to an LLM for disambiguation.

```
Prompt sent to LLM (Claude/GPT-4):
  "You are a financial data expert.
   Given the following SQL column context, identify which canonical financial metric it represents.

   Table: fund_metrics
   Column: money_on_money
   Data type: NUMERIC(8,4)
   Sample values: [2.38, 1.92]
   Co-occurring columns: internal_rate_return_net, distributions_over_contributions,
                         total_value_over_contributions, enterprise_value

   Canonical metrics to choose from:
   - NetIRR: Net Internal Rate of Return (range 0.0-1.0, decimal)
   - GrossIRR: Gross Internal Rate of Return (range 0.0-1.0, decimal)
   - MOIC: Multiple on Invested Capital (range 1.0-10.0)
   - DPI: Distributions to Paid-In Capital (range 0.0-5.0)
   - TVPI: Total Value to Paid-In Capital (range 0.0-10.0)
   - NAV: Net Asset Value (large dollar amount)

   Identify the metric and explain your reasoning."

LLM response:
  "MOIC. 'Money on money' is a colloquial term for Multiple on Invested Capital.
   The values [2.38, 1.92] confirm this is a return multiple (>1.0), not a rate (<1.0).
   Confidence: very high."

→ Signal confidence: 0.96
```

---

### Confidence Scoring and Decision

All six signals are combined with a weighted formula:

```
Final Confidence =
  0.25 × token_keyword_match      (domain knowledge)
  0.20 × value_range_plausibility (data evidence)
  0.20 × context_co_occurrence    (structural pattern)
  0.20 × embedding_similarity     (semantic distance)
  0.10 × fuzzy_string_match       (lexical distance)
  0.05 × llm_classification       (LLM, only if triggered)

Example for irr_net:
  = 0.25 × 0.91
  + 0.20 × 0.95
  + 0.20 × 0.97
  + 0.20 × 0.94
  + 0.10 × 0.85
  + 0.05 × 0.00   (LLM not triggered, confidence already high)
  = 0.228 + 0.190 + 0.194 + 0.188 + 0.085 + 0.000
  = 0.885 → rounded with boost for co-occurrence pair → 0.97
```

**Decision thresholds:**

| Confidence | Action |
|-----------|--------|
| ≥ 0.90 | Auto-accept. Mapping created. Steward notified. |
| 0.75 – 0.89 | Suggested mapping. Data steward must approve. |
| 0.50 – 0.74 | Ambiguous. Steward must choose from top 3 candidates. |
| < 0.50 | Cannot auto-map. Manual mapping required. |

---

### Human-in-the-Loop and Learning

Every human-approved mapping becomes a training example:

```
Steward approves: citadel.money_on_money → MOIC
  → Stored as: {source: "money_on_money", canonical: "MOIC", approved_by: "john.smith", date: "2025-05-31"}
  → This example is added to the few-shot LLM prompt for future mappings
  → The abbreviation dictionary is updated: "money_on_money" → MOIC alias
  → Confidence threshold for "money_on_money" pattern raised to 0.98 in future
```

The system learns with every client onboarded. After 20 clients, most financial column names are already known.

---

## Question 2 — Why OWL 2? Is There Something Simpler?

### Short Answer: Yes. Start Simple. Here Is the Full Spectrum.

OWL 2 is the most powerful but also the most complex option. For a production platform serving multiple teams, **start with Level 1 (Simple JSON Registry) and evolve from there**. OWL 2 is Level 4 — for organizations with dedicated ontology engineers.

---

### The Concept Registry Spectrum

```
Level 0 — Just a database table (5 minutes to implement)
Level 1 — JSON/YAML concept files (1 day to implement, recommended start)
Level 2 — JSON-LD (adds linked data without OWL complexity)
Level 3 — SKOS (W3C standard for vocabularies, no reasoning needed)
Level 4 — OWL 2 (formal reasoning, full axiomatization — production for mature orgs)
```

---

### Level 0 — Plain Database Table (Simplest)

```sql
-- Just a PostgreSQL table. Start here.
CREATE TABLE concepts (
    concept_id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name         VARCHAR(200) NOT NULL,
    domain       VARCHAR(100) NOT NULL,
    definition   TEXT,
    parent_id    UUID REFERENCES concepts(concept_id),
    created_by   VARCHAR(200),
    created_at   TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE concept_synonyms (
    concept_id   UUID REFERENCES concepts(concept_id),
    synonym      VARCHAR(200) NOT NULL,
    synonym_type VARCHAR(50) DEFAULT 'acceptable'  -- preferred | acceptable | deprecated
);

-- Insert the financial concepts
INSERT INTO concepts (name, domain, definition) VALUES
  ('NetIRR',    'private-markets', 'Net Internal Rate of Return after fees and carry'),
  ('GrossIRR',  'private-markets', 'Gross Internal Rate of Return before fees'),
  ('MOIC',      'private-markets', 'Multiple on Invested Capital'),
  ('DPI',       'private-markets', 'Distributions to Paid-In Capital'),
  ('TVPI',      'private-markets', 'Total Value to Paid-In Capital');

INSERT INTO concept_synonyms VALUES
  ((SELECT concept_id FROM concepts WHERE name='NetIRR'), 'irr_net',                    'deprecated'),
  ((SELECT concept_id FROM concepts WHERE name='NetIRR'), 'net_irr_pct',                'deprecated'),
  ((SELECT concept_id FROM concepts WHERE name='NetIRR'), 'internal_rate_return_net',   'deprecated'),
  ((SELECT concept_id FROM concepts WHERE name='NetIRR'), 'Net Internal Rate of Return','preferred'),
  ((SELECT concept_id FROM concepts WHERE name='MOIC'),   'return_multiple',             'deprecated'),
  ((SELECT concept_id FROM concepts WHERE name='MOIC'),   'money_on_money',              'deprecated');
```

**Who should use this:** Any team starting out. This is production-ready and covers 90% of use cases.

**Limitation:** No formal parent-child reasoning. No machine-readable semantics. Works great for humans, okay for AI.

---

### Level 1 — YAML Concept Files (Recommended Production Start)

```yaml
# File: concepts/private-markets/performance-metrics.yaml
# Version controlled in Git. Reviewed via pull request. Human-readable.

concepts:
  - id: "pm:NetIRR"
    name: "Net IRR"
    domain: "private-markets.performance"
    definition: >
      The Internal Rate of Return of a fund calculated net of all fees
      (management fee, carried interest). Expressed as a decimal fraction.
      A Net IRR of 0.234 means 23.4% annualized net return.
    parent: "pm:PerformanceMetric"
    data_type: "decimal_percentage"
    typical_range: [0.0, 0.5]
    synonyms:
      preferred:
        - "Net Internal Rate of Return"
        - "Net IRR"
        - "Fund Net IRR"
      acceptable:
        - "IRR Net"
        - "Net Return Rate"
      deprecated:
        - "irr_net"          # Apex Capital SQL column
        - "net_irr_pct"      # Blue Ridge SQL column
        - "internal_rate_return_net"  # Citadel SQL column
        - "money_on_money"   # wrong metric, but sometimes confused
      abbreviation:
        - "IRR (net)"
    related:
      - "pm:GrossIRR"       # gross version of same concept
      - "pm:MOIC"           # complementary performance metric
    notes: >
      Net IRR and Gross IRR are always reported together.
      Net IRR is always lower than Gross IRR.
      Typical PE fund Net IRR benchmark: 15-20%.

  - id: "pm:MOIC"
    name: "MOIC"
    domain: "private-markets.performance"
    definition: >
      Multiple on Invested Capital. Total value of an investment
      (realized + unrealized) divided by total capital invested.
      A MOIC of 2.5x means the investment is worth 2.5 times the amount invested.
    parent: "pm:PerformanceMetric"
    data_type: "multiple"
    typical_range: [1.0, 10.0]
    synonyms:
      preferred:
        - "MOIC"
        - "Multiple on Invested Capital"
        - "Investment Multiple"
      acceptable:
        - "Return Multiple"
        - "Gross MOIC"
        - "Total Return Multiple"
      deprecated:
        - "return_multiple"     # Blue Ridge SQL column
        - "money_on_money"      # Citadel SQL column (informal term)
      abbreviation:
        - "MoM"                 # money-on-money abbreviation
    notes: >
      For realized investments: MOIC = Realized Value / Invested Capital.
      For unrealized: MOIC = (Unrealized FMV + Distributions) / Invested Capital.
      MOIC and TVPI are the same metric when used for a single investment.
```

**Why YAML files:**
- Version controlled in Git — full history, code review process
- Human-readable — any analyst can read and edit
- Structured enough for the platform to parse and index
- No special tooling required — just a text editor
- Pull request for any concept change → governance built-in
- **This is what DataHub, Amundsen, OpenMetadata, and Backstage all use**

**Implementation:** The platform reads these files at startup, loads concepts into PostgreSQL, and embeds definitions for semantic search.

---

### Level 2 — JSON-LD (Linked Data Without the Complexity)

```json
{
  "@context": {
    "pm": "https://kop.platform/ontology/private-markets/",
    "schema": "https://schema.org/",
    "definition": "schema:description",
    "name": "schema:name"
  },
  "@id": "pm:NetIRR",
  "@type": "pm:PerformanceMetric",
  "name": "Net IRR",
  "definition": "Net Internal Rate of Return after fees.",
  "pm:synonyms": ["irr_net", "net_irr_pct", "internal_rate_return_net"],
  "pm:typicalRange": {"pm:min": 0.0, "pm:max": 0.5},
  "pm:relatedTo": "pm:GrossIRR"
}
```

**Use when:** You need the concepts to be machine-readable by external systems (APIs, semantic web tools) but do not need formal reasoning. Good for interoperability.

---

### Level 3 — SKOS (W3C Standard, Simple, Production-Ready)

```turtle
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix pm: <https://kop.platform/ontology/private-markets/> .

pm:NetIRR a skos:Concept ;
    skos:prefLabel "Net IRR"@en ;
    skos:altLabel "Net Internal Rate of Return"@en ;
    skos:altLabel "irr_net"@en ;
    skos:definition "IRR of a fund net of management fees and carried interest."@en ;
    skos:broader pm:PerformanceMetric ;
    skos:related pm:GrossIRR ;
    skos:note "Values are expressed as decimals: 0.234 = 23.4%"@en .
```

**SKOS is:**
- A W3C standard (stable, widely supported)
- Simpler than OWL — no formal reasoning required
- Supported by tools: Protégé (simplified), VocBench, PoolParty, TopBraid
- Used by: Library of Congress, Getty Institute, UN FAO, European Commission
- **Good production choice for knowledge platforms that need interoperability but not reasoning**

---

### Level 4 — OWL 2 (Full Power, Maximum Complexity)

OWL 2 adds:
- **Class restrictions** (a Fund must have at least one PortfolioCompany)
- **Property axioms** (NetIRR is always less than GrossIRR — formally stated)
- **Automated reasoning** (infer new facts from stated facts)
- **Consistency checking** (detect logical contradictions in your concept model)

**Use when:**
- You have dedicated ontology engineers
- You need automated reasoning (OWL reasoners: HermiT, Pellet, ELK)
- You are integrating with industry standards (FIBO, SNOMED, ICD-11) that are already in OWL
- Healthcare, banking regulation, or pharma domains where formal semantics are required

**Do NOT use OWL 2 as your starting point.** Migrate to it when you have a stable SKOS/YAML model and a real business need for formal reasoning.

---

### Recommendation for this Platform

```
Month 1-3:   Level 1 (YAML concept files, PostgreSQL registry)
Month 4-6:   Level 2 (JSON-LD for API responses)
Month 7-12:  Level 3 (SKOS for vocabulary management — use PoolParty or VocBench)
Year 2+:     Level 4 (OWL 2 for specific domains like banking FIBO or healthcare SNOMED)
```

The platform architecture supports all levels. Teams choose their level. The API surface is the same regardless of which level the backend uses.

---

## Question 3 — Taxonomy: How Is It Designed, and What Algorithms Help?

### What Taxonomy Solves

Taxonomy answers: **"How do we classify things into groups?"**

In the private markets example:
- Apex says "Software"
- Blue Ridge says "Technology"  
- Citadel uses GICS code "45101010"
- All mean the same sector

The taxonomy is the hierarchy that all three map into. Building it and keeping it current is a design problem.

---

### Three Strategies — Teams Choose

---

#### Strategy 1 — Top-Down: Start from an Industry Standard

Pick an existing classification system as your taxonomy skeleton.

```
Private Markets options:
  GICS  — Global Industry Classification Standard (MSCI + S&P) — 11 sectors, 24 groups, 69 industries
  NAICS — North American Industry Classification System — 20 sectors
  SIC   — Standard Industrial Classification — older, US-focused
  NACE  — European industry classification (Rev. 2)
  BVCA  — British Private Equity sector classification
  PitchBook — venture/PE specific sector taxonomy

Healthcare:
  SNOMED hierarchy (conditions, procedures, substances)
  ICD-11 chapter structure

Banking:
  FIBO product classification
```

**How to implement:**

```python
# Load GICS taxonomy from official source
gics_taxonomy = {
  "10": {"name": "Energy",    "groups": {
    "1010": {"name": "Energy", "industries": {
      "101010": {"name": "Energy Equipment & Services"},
      "101020": {"name": "Oil, Gas & Consumable Fuels"}
    }}
  }},
  "45": {"name": "Information Technology", "groups": {
    "4510": {"name": "Software & Services", "industries": {
      "451010": {"name": "IT Services"},
      "451020": {"name": "Software"}
    }},
    "4520": {"name": "Technology Hardware", "industries": {
      "452010": {"name": "Communications Equipment"},
      "452020": {"name": "Technology Hardware, Storage & Peripherals"}
    }}
  }}
}

# Then map each client's source values to GICS nodes
source_to_gics = {
  "Software":                ("45", "4510", "451020"),  # GICS Software
  "Technology":              ("45", None, None),         # GICS IT (broad)
  "45101010":                ("45", "4510", "451010"),   # GICS IT Services (exact)
  "Internet & Digital":      ("45", "4510", "451020"),   # closest GICS
  "Life Sciences":           ("35", "3520", "352020"),   # Pharmaceuticals
}
```

**Pros:** Authoritative. Agreed-upon by industry. Cross-client comparisons work immediately.
**Cons:** May not fit every client's nuances. GICS has 11 sectors — too broad for some use cases.

---

#### Strategy 2 — Bottom-Up: Let the Data Tell You the Taxonomy

Collect all unique sector/category values from all clients, then cluster them automatically.

**Step 1: Collect all values**
```
From all clients, collect every unique sector/category value:
  "Software", "Technology", "Healthcare", "Life Sciences", "Clean Energy",
  "Industrials", "45101010", "35202010", "20101010", "Fintech",
  "Financial Services", "Consumer", "Business Services", "Media",
  "Real Estate", "Infrastructure", "Energy", "Materials"
  ... (could be hundreds across many clients)
```

**Step 2: Embed all values**
```python
# Embed every unique value using text-embedding-3-large
embeddings = {
  "Software":           [0.234, -0.189, ...],  # 3072-dim vector
  "Technology":         [0.241, -0.182, ...],  # very similar to Software
  "45101010":           [0.238, -0.185, ...],  # GICS code, decoded as "IT Services"
  "Life Sciences":      [0.102,  0.341, ...],  # different cluster
  "Healthcare":         [0.098,  0.352, ...],  # close to Life Sciences
  "Industrials":        [-0.121, 0.089, ...],  # different cluster entirely
  "Clean Energy":       [-0.089, -0.234, ...], # another cluster
}
```

**Step 3: Cluster the embeddings**
```python
from sklearn.cluster import AgglomerativeClustering
import numpy as np

vectors = np.array(list(embeddings.values()))
labels = list(embeddings.keys())

# Hierarchical clustering builds a natural tree structure
clustering = AgglomerativeClustering(
    n_clusters=None,
    distance_threshold=0.3,   # tune this: smaller = more clusters
    linkage='ward'
)
cluster_ids = clustering.fit_predict(vectors)

# Result (example):
# Cluster 0: ["Software", "Technology", "45101010", "Internet & Digital"]
# Cluster 1: ["Life Sciences", "Healthcare", "Pharma", "35202010"]
# Cluster 2: ["Industrials", "Manufacturing", "20101010"]
# Cluster 3: ["Clean Energy", "Renewables", "Sustainable Infrastructure"]
# Cluster 4: ["Fintech", "Financial Services", "Financial Technology"]
```

**Step 4: Human names the clusters**
```
The platform shows the data steward each cluster with its members.
Steward assigns canonical names:

Cluster 0 → "Technology"
Cluster 1 → "Healthcare & Life Sciences"
Cluster 2 → "Industrials"
Cluster 3 → "Clean Energy & Sustainability"
Cluster 4 → "Financial Services & Fintech"
```

**Pros:** Taxonomy emerges from the actual data. No upfront design needed. Finds terms you didn't know clients used.
**Cons:** Clusters may not align with industry conventions. Requires human review. May need re-clustering as new clients join.

---

#### Strategy 3 — Hybrid (Recommended for Multi-Tenant SaaS)

```
Step 1: Import a standard taxonomy skeleton (GICS or industry-specific)
         → This gives you the Level 1 and Level 2 nodes immediately

Step 2: Run bottom-up clustering on all client values
         → Cluster output shows: which values already map to standard nodes,
           and which values don't fit anywhere

Step 3: For values that fit standard nodes → auto-map with confidence score
         → "Software" → GICS 451020 (Software) → confidence 0.97

Step 4: For values that don't fit → propose new taxonomy node extension
         → "Fintech" doesn't map cleanly to any GICS node
         → Platform proposes: "Technology > Financial Technology (Fintech)" as new node
         → Data steward approves → permanent taxonomy extension

Step 5: GICS code lookup for structured codes
         → "45101010" → decode via GICS reference table → "Internet Software & Services"
         → Map to Technology > Software & Services → confidence 0.99
```

---

### Algorithms for Source Value → Taxonomy Node Mapping

Once the taxonomy exists, how does the platform decide which source value belongs in which node?

| Method | Use case | Confidence |
|--------|----------|-----------|
| **Exact string match** | "Industrials" → Industrials node | 1.00 |
| **Case-insensitive match** | "industrials" → Industrials | 1.00 |
| **Standard code lookup** | "45101010" → GICS reference → Technology | 0.99 |
| **Fuzzy string (Jaro-Winkler)** | "Techonlogy" (typo) → Technology | 0.95 |
| **Embedding cosine similarity** | "IT Services" → Technology cluster | 0.92 |
| **Parent expansion** | "iOS App Development" → Software → Technology | 0.88 |
| **LLM classification** | "SaaS B2B" → Technology > Software | 0.90 |
| **Human override** | Steward maps any value manually | 1.00 |

---

### What Teams Can Configure

The platform lets each team choose their taxonomy strategy via configuration:

```yaml
# taxonomy-config.yaml for apex-capital tenant
taxonomy:
  strategy: hybrid                     # top_down | bottom_up | hybrid

  base_taxonomy: gics_2023             # use GICS as the skeleton
  
  custom_nodes:                        # tenant-specific extensions
    - name: "Fintech"
      parent: "Technology"
      description: "Financial technology companies"
    - name: "PropTech"
      parent: "Real Estate"
      description: "Real estate technology companies"

  source_mappings:                     # manual overrides (highest priority)
    - source_value: "Software (ARR > $10M)"
      taxonomy_node: "Technology"
      confidence: 1.0

  auto_mapping:
    enabled: true
    confidence_threshold: 0.85         # auto-accept above 0.85
    review_threshold: 0.65             # flag for review between 0.65-0.85
    embedding_model: text-embedding-3-large
    enable_llm_fallback: true          # use LLM for < 0.65 confidence

  governance:
    require_steward_approval: true     # for new taxonomy nodes
    allow_tenant_extensions: true      # can add nodes below global nodes
```

---

## Question 4 — Semantic Layer and Vector Chunking: What Is the Use If There Is No Definition?

### First: Understand the Difference Between Semantic and Vector

These are two different things that work together but serve different purposes.

```
Semantic Layer = The MEANING layer (what does "IRR" mean?)
Vector Search  = The FINDING layer (where is the thing you're looking for?)

Semantic helps vector become more accurate.
But vector works EVEN WITHOUT semantic.
```

---

### What Happens Without Any Definition (Zero Metadata State)

Imagine you just connected Apex Capital's SQL Server. You have:
- 3 tables
- 9 columns in `fund_performance`
- No definitions anywhere
- No glossary terms
- No ontology

**Can the platform still provide value? YES.**

Here is what the vector plane does with zero definitions:

```python
# Auto-constructed embedding text for irr_net column (no definition needed):
embedding_text = """
Column: irr_net
Table: fund_performance
Database: apex_capital_db
Data type: DECIMAL(8,4)
Sample values: 0.234, 0.182
Co-occurring columns: irr_gross, moic, dpi, tvpi, nav_usd, reporting_date
Table row count: 2
"""

# This text is embedded into a vector → stored in Qdrant

# Now user searches: "show me fund returns"
# Platform embeds query → "fund returns" vector
# Cosine similarity finds: irr_net, irr_gross, moic → all close in vector space
# Result: system finds the right columns even with ZERO definitions
```

The vectors encode the **structural semantics** (column name + data type + co-occurrence) even without human-written definitions. This is why Google can find documents even when the documents have no descriptions.

---

### The Value Progression: From Zero to Full Definitions

```
Stage 0: Raw ingestion only (no definitions, no enrichment)
  Vector content: column name + data type + sample values + table context
  Search quality: ~60%  (finds roughly the right thing, misses edge cases)
  Use: "find anything that looks like fund performance data"

Stage 1: Auto-generated descriptions (LLM generates candidate definitions)
  Vector content: same as Stage 0 + LLM-generated description
  "This column irr_net in fund_performance likely represents Net Internal Rate
   of Return, a measure of fund performance after fees, expressed as a decimal."
  Search quality: ~80%  (much better — semantic content is richer)
  Use: "find Net IRR data" → finds irr_net, net_irr_pct, internal_rate_return_net

Stage 2: Canonical mapping applied (no human definition yet, but mapping exists)
  Vector content: same + canonical name applied
  "Column irr_net → canonical: NetIRR. Part of fund performance metrics group."
  Search quality: ~85%  (canonical grouping makes cluster-level search possible)
  Use: "compare IRR across all funds" → all three client columns found

Stage 3: Human-approved glossary term (definition exists, approved by steward)
  Vector content: full definition embedded separately + linked to column vectors
  "Net IRR: Net Internal Rate of Return after management fees and carried interest.
   Synonyms: irr_net, net_irr_pct, internal_rate_return_net, return_rate_net.
   Domain: private-markets.performance. Typical range: 5%-40%."
  Search quality: ~95%  (semantic distance to query is now very accurate)
  Use: "what is the annualized return after fees for my funds?" → finds Net IRR

Stage 4: Full ontology concept (OWL/SKOS formal definition)
  Vector content: same as Stage 3 + relationship context
  "NetIRR is a subclass of PerformanceMetric. Related to GrossIRR (gross version).
   Prerequisite: cash flow data (calls + distributions). Per FIBO ontology."
  Search quality: ~98%  (relationship-aware retrieval)
  Use: AI reasoning over concept graph
```

**The key insight: you start at Stage 0 on Day 1 and get immediate value. Definitions make it better but are not required to begin.**

---

### What Is Chunking and When Does It Apply?

Chunking is specifically about **unstructured documents** (PDFs, Word files, web pages), not structured database tables.

```
Structured data (SQL tables):
  Unit of storage = one row or one column description
  Chunking = NOT needed (the row IS the chunk)
  Each row becomes one vector point in Qdrant
  Example: fund_performance row APX-F1 → one vector

Unstructured data (documents, PDFs):
  Unit of storage = paragraph or section
  Chunking = REQUIRED
  A 50-page CIM document cannot fit in one vector — you must break it into pieces
```

**Why chunking matters for documents:**

```
Without chunking (whole document as one vector):
  Document: "Apex Capital CIM — 50 pages about TechFlow Inc"
  One vector for all 50 pages
  
  Problem: The vector averages all the content
  Query: "What is TechFlow's revenue growth rate?"
  → Vector similarity finds the CIM (good!)
  → But returns the ENTIRE 50-page document (bad)
  → LLM context window: 8,000 tokens → 50 pages don't fit
  → Answer quality: poor (relevant paragraph diluted by 50 pages of noise)

With chunking (split into paragraphs/sections):
  Document: split into 180 chunks of ~200 words each
  180 vectors stored, each covering one section
  
  Chunk 47: "TechFlow's ARR grew from $8.2M to $14.7M (79% growth) in FY2024..."
  Chunk 48: "The company's gross margin expanded from 71% to 78%..."
  
  Query: "What is TechFlow's revenue growth rate?"
  → Vector similarity finds Chunk 47 specifically (not the whole 50 pages)
  → LLM context: 200 words of exactly the right section
  → Answer quality: excellent and precise
```

---

### Chunking Strategies — Which to Use When

| Strategy | How it works | Best for |
|----------|-------------|---------|
| **Fixed size** | Split every N words (e.g., 200 words) | Simple. Works for most unstructured text. |
| **Sentence** | Split on sentence boundaries | Short, factual documents |
| **Paragraph** | Split on paragraph boundaries | Reports, memos, CIMs |
| **Section** | Split on headings (H1/H2/H3) | Structured reports, prospectuses |
| **Semantic** | Group sentences until topic changes | Best quality, most complex |
| **Recursive** | Try section → paragraph → sentence in order | Documents with mixed structure |

**For Private Markets documents:**
```
CIM (Confidential Information Memorandum):
  Strategy: Section chunking (by headings) + overlap 50 words
  Sections: Executive Summary, Business Overview, Financial Performance,
            Market Opportunity, Management Team, Investment Thesis
  Result: Each section is one chunk → semantically coherent

Fund Prospectus (PPM):
  Strategy: Paragraph chunking with 20% overlap
  Overlap reason: Risk factors often span paragraphs

LP Reports (quarterly):
  Strategy: Fixed table rows for financial data + paragraph for commentary
  Hybrid: structured rows as individual vectors, text as paragraph chunks
```

**Overlap explained:**
```
Without overlap:
  Chunk 1: "TechFlow's revenue in FY2024 was $14.7M. The company achieved"
  Chunk 2: "79% growth compared to FY2023 when revenue was $8.2M."

  Problem: "What was TechFlow's growth rate?" 
  → The answer spans both chunks. Neither chunk alone is the best result.

With 20-word overlap:
  Chunk 1: "TechFlow's revenue in FY2024 was $14.7M. The company achieved 79% growth"
  Chunk 2: "The company achieved 79% growth compared to FY2023 when revenue was $8.2M."

  Solution: Both chunks now contain the full fact → search finds the best one.
```

---

### Putting It All Together: Semantic + Vector + Chunking in the Full Flow

```
                    PRIVATE MARKETS DATA TYPES AND HOW EACH IS HANDLED
                    ─────────────────────────────────────────────────────

Data Type           | Semantic Layer Role          | Vector Storage          | Chunking?
--------------------|------------------------------|-------------------------|----------
SQL table column    | Maps irr_net → NetIRR        | One vector per column   | No
SQL table row       | Canonical values applied     | One vector per row      | No
Fund prospectus PDF | Glossary terms link to sections | One vector per section | Yes (by section)
CIM document        | Investment term definitions  | One vector per paragraph | Yes (by paragraph)
LP quarterly report | Metric definitions for tables | Tables: row vectors, text: para vectors | Yes for text
Research report     | Domain terminology for boost | One vector per paragraph | Yes
Email (executive)   | Named entity recognition     | One vector per email    | Maybe (if long)
Meeting transcript  | Entity + topic tagging       | One vector per ~300 words | Yes
```

---

### The Simplest Mental Model

```
Think of the platform as a very smart librarian.

Without definitions (Stage 0):
  Librarian has seen the books but hasn't read them.
  Librarian can find books about "fund performance" because 
  the title and table of contents use those words.
  Success rate: ~60%

With auto-descriptions (Stage 1):
  Librarian has skimmed every chapter heading and first paragraph.
  Can now find the specific chapter about IRR even if you say "return after fees."
  Success rate: ~80%

With full definitions (Stage 3):
  Librarian has read every book and memorized every synonym, 
  alias, and related concept.
  You say "annualized return net of carry" → librarian instantly 
  knows you mean Net IRR and finds every document about it.
  Success rate: ~95%

Chunking = the librarian opens the book and finds the right PAGE,
            not just the right book.

Without chunking: "It's in this 400-page book somewhere."
With chunking:    "Page 47, third paragraph — here is exactly what you asked for."
```

---

## Summary: Decisions and Recommendations

| Question | Simple Recommendation |
|----------|----------------------|
| **Canonical mapping algorithm** | Use all 6 signals. Start with token matching + value range + embedding similarity. Add LLM fallback for ambiguous cases. Human approval for < 0.90 confidence. |
| **Ontology/Concept format** | Start with YAML concept files (Level 1). They are version-controllable, human-readable, and production-ready. Migrate to SKOS when you need interoperability. OWL 2 only for specific domains later. |
| **Taxonomy design** | Use hybrid strategy: import GICS as skeleton, run embedding clustering on client data to find unmapped values, let stewards name the clusters. Teams configure confidence thresholds. |
| **Semantic + Vector without definitions** | Start embedding immediately — even column names + statistics provide 60% search quality. Definitions upgrade quality to 95% but are not a prerequisite. Chunking only applies to unstructured documents, not SQL rows. |
