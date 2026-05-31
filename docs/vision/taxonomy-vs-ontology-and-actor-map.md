# Taxonomy vs Ontology — and Who Does What
## Two Questions Answered With Zero Ambiguity

---

## Part 1 — Taxonomy vs Ontology: When Do You Need Which?

### One-Line Difference

```
Taxonomy  = How do you ORGANIZE things into groups?     (classification)
Ontology  = What do things MEAN and how do they RELATE? (definition + relationships)
```

They solve different problems. You can use one without the other. Or both together.

---

### Understand the Difference With One Example

Imagine you have 100 portfolio companies. You want to:

**Task A:** Show a dropdown filter in the UI — "Filter by Sector"
→ You need a list of sectors with parent-child structure
→ You need **Taxonomy only**

**Task B:** The AI should understand that "Net IRR" and "irr_net" and "return after fees" all mean the same thing
→ You need definitions and synonyms for concepts
→ You need **Ontology / Semantic Glossary only**

**Task C:** You want to say "TechFlow Inc belongs to Technology sector, and Technology sector means companies whose primary business is software and IT services"
→ You need to classify (taxonomy) AND define the classification node (ontology)
→ You need **Both**

---

### Decision Framework — 4 Questions

Ask yourself these four questions. Each "yes" tells you what you need.

```
Q1: Do I need to ORGANIZE or GROUP things into a hierarchy?
    (e.g., sectors, document types, geographies, product categories)
    YES → You need TAXONOMY

Q2: Do I need to DEFINE what concepts MEAN?
    (e.g., what is "Net IRR"? what is a "Portfolio Company"?)
    YES → You need ONTOLOGY (or Semantic Glossary — same idea, different formality)

Q3: Do I need to model RELATIONSHIPS between concepts?
    (e.g., "Net IRR is a type of Performance Metric",
           "A Fund has many Portfolio Companies",
           "Net IRR is always less than Gross IRR")
    YES → You need ONTOLOGY

Q4: Do I need AUTOMATED REASONING over concepts?
    (e.g., "If a company has revenue growth > 50%, classify it as High Growth")
    YES → You need FORMAL ONTOLOGY (OWL 2)
```

---

### Decision Table — Concrete Use Cases

| Use Case | Taxonomy | Ontology | Both | Why |
|----------|----------|----------|------|-----|
| UI filter: "show companies by sector" | ✅ | ❌ | | Just grouping. No definitions needed. |
| Faceted search: "filter by document type" | ✅ | ❌ | | Hierarchy for navigation only. |
| Normalize sector names across clients | ✅ | ❌ | | Map "Software", "Technology", "45101010" to one node. |
| Define what "Net IRR" means | ❌ | ✅ | | Concept definition + synonyms. |
| AI understands "money on money" = MOIC | ❌ | ✅ | | Synonym mapping. No grouping needed. |
| Model: Fund → has → PortfolioCompany | ❌ | ✅ | | Relationship modeling. Not a hierarchy. |
| Cross-client metric comparison (IRR) | ❌ | ✅ | | Canonical concept, not a category. |
| Classify companies AND explain what "Technology" means | | | ✅ | Taxonomy node gets an ontology definition. |
| Browse documents by type AND AI understands document types | | | ✅ | Both classification and meaning. |
| Build a "top quartile" inference rule | ❌ | ✅ | | Formal reasoning over concept constraints. |
| Regulatory compliance tagging | ✅ | ✅ | | Classify data (taxonomy) + define what each regulation means (ontology). |
| Search: "find healthcare investments" | ✅ | | | Taxonomy maps "Life Sciences", "Pharma", GICS codes to "Healthcare". |
| Search: "what is our exposure to ESG risk?" | ❌ | ✅ | | Concept definition + synonym resolution ("ESG", "sustainability risk", "green risk"). |
| Guided data entry (pick from a list) | ✅ | ❌ | | Controlled vocabulary = flat taxonomy. |

---

### When Taxonomy Alone Is Enough

**Use only taxonomy when:**
- Your problem is purely about organizing things into named buckets
- You need a hierarchy (parent → child)
- You need to drive UI filters, dropdowns, or browse navigation
- You are normalizing free-text category values across systems
- You do NOT need the platform to "understand" what those categories mean

**Private markets examples:**
- Sector hierarchy: Technology > Software > SaaS
- Geography: Americas > North America > United States > New York
- Strategy: Equity > Growth Equity / Buyout / Venture
- Document type: Report > Quarterly Report / Annual Report / CIM

**A taxonomy is just a structured list with parent-child relationships.** Nothing more.

---

### When Ontology (Semantic Glossary) Alone Is Enough

**Use only ontology when:**
- Your problem is about defining what things mean
- You have synonyms and aliases that confuse systems or people
- AI needs to understand your domain vocabulary
- You need to model relationships between concepts (not categories)
- You are building a business glossary

**Private markets examples:**
- Define: Net IRR, Gross IRR, MOIC, DPI, TVPI, NAV, FMV
- Map synonyms: `irr_net` = `net_irr_pct` = `internal_rate_return_net` = "Net IRR"
- Model: "A Fund has Performance Metrics"
- Model: "Net IRR is always ≤ Gross IRR"
- Define: "Portfolio Company is a company in which the fund has invested"

**You do NOT need a hierarchy for this.** Ontology is a concept graph, not a tree.

---

### When You Need Both

**Use both when:**
- Every node in your taxonomy needs a formal definition
- Taxonomy classification is used to drive AI reasoning
- You want to search both "things that belong to Technology" AND "things that relate to the concept Technology"
- You are doing regulatory compliance where categories have legal definitions

**Private markets example:**
```
Taxonomy node: "Technology"
  + Ontology definition: "Companies whose primary revenue comes from software,
    hardware, or IT services. GICS sectors 45 (Information Technology).
    Characterized by: high gross margins (>60%), scalable business model,
    recurring revenue preferred."
  + Ontology relationship: Technology isSubclassOf IndustrySector
  + Ontology property: Technology hasTypicalGrossMargin ">60%"

Now the platform can:
  1. Group companies by taxonomy node "Technology" (for filters) AND
  2. Let AI answer "what characterizes a technology investment?" (from definition) AND
  3. Let AI reason "if a company has 75% gross margin in Software, it fits Technology sector"
```

---

### Summary: The Simple Decision Rule

```
                    START HERE
                        │
         ┌──────────────┼──────────────┐
         │              │              │
         ▼              ▼              ▼
   Need to GROUP   Need to DEFINE  Need BOTH
   things into     what things     (group AND define)
   categories?     mean?
         │              │              │
         ▼              ▼              ▼
    TAXONOMY        ONTOLOGY /      TAXONOMY
    only            SEMANTIC        + ONTOLOGY
                    GLOSSARY only
```

**Rule of thumb for private markets SaaS:**
- Classification/filtering in UI → Taxonomy
- Metric definitions and synonyms (IRR, MOIC, etc.) → Semantic Glossary (lightweight ontology)
- Formal domain modeling (Fund has Portfolio Companies, etc.) → Ontology
- Complex reasoning rules → OWL 2 (later phase)

---

---

## Part 2 — Who Does What: The Complete Actor Map

There are **5 actors** in the platform. Each does a clearly defined set of things. Some tasks are automatic (zero humans), some are configured once, some require ongoing human judgment.

---

### The 5 Actors

```
Actor 1: THE PLATFORM (automated code + algorithms + LLM)
         → Runs 24/7 with zero human involvement
         → Does the heavy lifting

Actor 2: DATA ENGINEER / INTEGRATION TEAM
         → One-time setup per data source or new client
         → Provides connection details and scope
         → Does NOT write definitions or business logic

Actor 3: DATA STEWARD
         → Ongoing governance role (part-time, ~2-4 hrs/week per tenant)
         → Reviews and approves what the platform could not auto-decide
         → Domain expert for the business vocabulary

Actor 4: DOMAIN EXPERT / BUSINESS ANALYST
         → Infrequent (quarterly or on new domain setup)
         → Writes the authoritative concept definitions
         → Decides taxonomy strategy

Actor 5: PLATFORM ADMIN / TENANT ADMIN
         → Manages access, roles, tenant config
         → Does not touch data or definitions
```

---

### The Actor Map — Full Detail

```
TASK                                   WHO DOES IT        HOW              FREQUENCY
──────────────────────────────────────────────────────────────────────────────────────

─── CLIENT ONBOARDING ───────────────────────────────────────────────────────────────

Create tenant in platform              DATA ENGINEER      CLI / API call   Once per client
  kop tenant create --name "apex"      [30 seconds]

Provide SQL Server connection details  DATA ENGINEER      YAML config      Once per source
  host, port, database, credentials    [15 minutes]

Define which tables are in scope       DATA ENGINEER      YAML config      Once per source
  tables: [fund_performance, ...]      [15 minutes]

Set sovereignty zone and tier          DATA ENGINEER      CLI config       Once per tenant
  sovereignty_zone: US                 [5 minutes]

Total onboarding effort by human:      DATA ENGINEER      30-45 minutes    Once per client


─── WHAT HAPPENS AUTOMATICALLY AFTER ONBOARDING (NO HUMAN) ──────────────────────────

Connect to SQL Server and test         PLATFORM           Automatic        Once at setup
Extract full schema (DDL)              PLATFORM           Automatic        Every sync
Extract data rows in batches           PLATFORM           Automatic        Daily / weekly
Detect column data types and ranges    PLATFORM           Automatic        Every sync
Compute data quality score             PLATFORM           Automatic        Every sync
Store raw data in S3                   PLATFORM           Automatic        Every sync
Emit ingestion events to Redis         PLATFORM           Automatic        Every sync
Create AssetMetadata record            PLATFORM           Automatic        Every sync
Compute column value statistics        PLATFORM           Automatic        Every sync
Auto-tag asset with domain labels      PLATFORM/LLM       Automatic        Once per asset
Create OpenSearch index document       PLATFORM           Automatic        Every sync
Generate candidate description for     LLM                Automatic        Once per asset
  columns with no human definition     [e.g., "irr_net likely represents
                                        Net Internal Rate of Return based
                                        on name tokens and value range"]


─── CANONICAL MAPPING ────────────────────────────────────────────────────────────────

Run token + embedding + value signals  PLATFORM           Automatic        Every new column
Compute confidence score               PLATFORM           Automatic        Every new column

If confidence ≥ 0.90:
  Create canonical mapping             PLATFORM           Automatic        Immediate
  Notify steward (FYI, not action)     PLATFORM           Automatic        Immediate
  Link column to canonical metric      PLATFORM           Automatic        Immediate

If confidence 0.75 – 0.89:
  Create DRAFT mapping                 PLATFORM           Automatic        Immediate
  Send to steward review queue         PLATFORM           Automatic        Immediate
  Steward sees: "net_irr_pct → NetIRR? DATA STEWARD       Review UI        Within 48 hrs
    Confidence 0.82. Approve/Reject."

If confidence < 0.75:
  Flag as unmapped                     PLATFORM           Automatic        Immediate
  Send to steward for manual mapping   PLATFORM           Automatic        Immediate
  Steward manually assigns canonical   DATA STEWARD       Review UI        Within 1 week
  Or: Data Engineer adds rule to       DATA ENGINEER      YAML config      As needed
    abbreviation dictionary

After any human approval:
  Save as training example             PLATFORM           Automatic        Immediate
  Raise confidence threshold           PLATFORM           Automatic        Immediate
  Apply same mapping to future         PLATFORM           Automatic        Next sync
    columns with same name pattern


─── TAXONOMY ─────────────────────────────────────────────────────────────────────────

Choose taxonomy strategy               DOMAIN EXPERT      Decision         Once per domain
  (top-down / bottom-up / hybrid)      [30 minutes]

Import standard taxonomy skeleton      DATA ENGINEER      CLI command      Once per domain
  kop taxonomy import gics.csv          [1 hour]
  (GICS, NAICS, or custom)

Run embedding clustering on all        PLATFORM           Automatic        On demand
  sector values across all clients

Show clusters to steward for naming    PLATFORM           Automatic        After clustering

Name the clusters                      DATA STEWARD       Review UI        2-4 hours
  "Cluster 0 = Technology"             or
                                       DOMAIN EXPERT

Build source value → taxonomy          PLATFORM           Automatic        Every new value
  mapping (exact + fuzzy + embedding)

If mapping confidence ≥ 0.90:
  Auto-accept mapping                  PLATFORM           Automatic        Immediate
  e.g., "Technology" → sec-technology

If mapping confidence < 0.90:
  Flag for steward review              PLATFORM           Automatic        Immediate
  "industry_sector='Tech Svcs'. Map    DATA STEWARD       Review UI        Within 48 hrs
   to Technology? Or create new node?"

Add new taxonomy node                  DATA STEWARD       Review UI        As needed
  (e.g., "Fintech" not in GICS)        or DATA ENGINEER   YAML config

Tenant-specific taxonomy extensions    DATA STEWARD       YAML config      As needed
  (private sub-categories)             or platform UI


─── ONTOLOGY / SEMANTIC GLOSSARY ────────────────────────────────────────────────────

Write concept definitions              DOMAIN EXPERT      YAML file / UI   Once per concept
  (who writes it: the person who         or DATA STEWARD
   knows what "Net IRR" means)

LLM auto-draft a candidate definition  LLM / PLATFORM     Automatic        Once per concept
  (when no definition exists yet)       "Candidate: Net IRR is likely the
                                         annualized return after fees based
                                         on the column name and co-located
                                         columns. Please review."

Review auto-drafted definition          DATA STEWARD       Review UI        As needed
  Approve / Edit / Reject

Add synonyms to a concept              DATA STEWARD       Review UI        As needed
  "also known as: irr_net, net_irr_pct" or DOMAIN EXPERT  YAML file

Publish concept (make it platform-wide) DATA STEWARD       Review UI        After approval
  Draft → Reviewed → Approved → Published

Link ontology concept to taxonomy node  DATA STEWARD       Review UI        As needed
  (optional enrichment)                  or DOMAIN EXPERT

Platform links glossary terms to        PLATFORM           Automatic        After publish
  matching columns (via canonical map)


─── VECTOR EMBEDDINGS ────────────────────────────────────────────────────────────────

Generate embeddings for all assets     PLATFORM           Automatic        Every sync
  (columns, rows, documents, glossary)

Choose embedding model                 DATA ENGINEER      YAML config      Once per tenant
  embedding_model: text-embedding-3-large

Re-embed when model upgrades           DATA ENGINEER      CLI command      On model change
  kop vector reembed --tenant apex      [triggers async job]
  Platform runs in background           PLATFORM          Automatic        After trigger

Register new embedding model           DATA ENGINEER      CLI / API        On model upgrade


─── SEARCH ───────────────────────────────────────────────────────────────────────────

OpenSearch index creation              PLATFORM           Automatic        On first sync
Index documents                        PLATFORM           Automatic        Every sync
Re-index on policy change              PLATFORM           Automatic        On policy event
Configure search strategies            DATA ENGINEER      YAML config      Once per tenant
  strategies: [hybrid, graph]


─── GOVERNANCE ───────────────────────────────────────────────────────────────────────

Configure tenant roles                 PLATFORM ADMIN     CLI / UI         Once per tenant
Assign user to role                    PLATFORM ADMIN     CLI / UI         Per new user
Set data classification rules          PLATFORM ADMIN     YAML config      Once per tenant
  default_classification: CONFIDENTIAL  or DATA STEWARD
Set sovereignty zone                   DATA ENGINEER      Config at setup  Once per tenant
Classify a specific asset              DATA STEWARD       Review UI        As needed
  (override auto-classification)
Approve access to RESTRICTED data      DATA STEWARD       Approval workflow On request
  (approval workflow)


─── NEW CLIENT ONBOARDING (SUMMARY) ─────────────────────────────────────────────────

What DATA ENGINEER does (manual):
  1. Create tenant                      [5 min]
  2. Configure SQL Server connector     [20 min]
  3. Specify table scope                [10 min]
  4. Set sovereignty zone               [5 min]
  Total: ~40 minutes of human work

What PLATFORM does (automatic after that):
  5. Connect and extract schema         [automatic]
  6. Extract data rows                  [automatic]
  7. Create metadata records            [automatic]
  8. Run canonical mapping (signals)    [automatic]
  9. Auto-accept high-confidence maps   [automatic]
  10. Flag low-confidence maps          [automatic, goes to steward queue]
  11. Generate LLM candidate definitions[automatic]
  12. Embed all assets                  [automatic]
  13. Index in OpenSearch               [automatic]
  14. Data is now searchable            [same day]

What DATA STEWARD does (after automatic steps):
  15. Review ~10-20 low-confidence mappings   [1-2 hours]
  16. Name any unrecognized taxonomy clusters [1 hour]
  17. Approve or edit LLM-drafted definitions [1-2 hours]
  Total: ~4 hours of human work

Total time from "new client" to "fully operational":  SAME DAY
Total human effort required:  ~5 hours (engineer 40 min + steward 4 hrs)
```

---

### One-Page Actor Summary

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           WHO DOES WHAT                                       │
├────────────────────┬─────────────────────────────────────────────────────────┤
│ ACTOR              │ WHAT THEY DO                                             │
├────────────────────┼─────────────────────────────────────────────────────────┤
│ PLATFORM           │ Everything that can be computed or decided automatically │
│ (code + LLM)       │ Ingestion, extraction, metadata, canonical mapping       │
│ AUTOMATIC          │ (high confidence), embedding, indexing, event routing,   │
│                    │ quality scoring, LLM-drafted definitions, clustering      │
│                    │ Runs 24/7. Zero human involvement for happy path.         │
├────────────────────┼─────────────────────────────────────────────────────────┤
│ DATA ENGINEER      │ One-time wiring of data sources                          │
│ CONFIGURE ONCE     │ SQL connector config, table scope, sovereignty zone,     │
│                    │ embedding model choice, search strategy config.           │
│                    │ Done per new client or new data source.                  │
│                    │ ~40 minutes per client. All in YAML / CLI.               │
├────────────────────┼─────────────────────────────────────────────────────────┤
│ DATA STEWARD       │ Review queue for things platform could not auto-decide   │
│ ONGOING GOVERNANCE │ Low-confidence canonical mappings (approve/reject)        │
│ (part-time)        │ Unmapped taxonomy values (assign to node)                │
│                    │ LLM-drafted definitions (edit and approve)               │
│                    │ Asset classification overrides                           │
│                    │ Access approval workflows                                │
│                    │ ~4 hrs/week for a 3-client deployment                    │
├────────────────────┼─────────────────────────────────────────────────────────┤
│ DOMAIN EXPERT      │ Authoritative business knowledge input                   │
│ INFREQUENT         │ Write the FIRST definition for a new concept domain      │
│                    │ Decide taxonomy strategy (GICS vs custom vs hybrid)      │
│                    │ Approve published ontology concepts                      │
│                    │ ~1 day per new domain onboarded (e.g., first PE client)  │
│                    │ Reused for all subsequent clients in same domain          │
├────────────────────┼─────────────────────────────────────────────────────────┤
│ PLATFORM ADMIN     │ Access management only                                   │
│ ADMIN ONLY         │ Create tenants, assign roles, set access policies        │
│                    │ Does NOT touch data, definitions, or mappings            │
└────────────────────┴─────────────────────────────────────────────────────────┘
```

---

### New Domain vs Repeat Domain

The key insight: **the first client in a domain is hard. Every client after that is easy.**

```
FIRST private markets client:
  ├── Data Engineer: configure SQL connector           [40 min]
  ├── Domain Expert: write concept definitions         [1 day]
  │     "What is Net IRR? MOIC? DPI? Portfolio Company?"
  ├── Data Steward: approve canonical mappings         [2 hrs]
  ├── Data Steward: name taxonomy clusters             [1 hr]
  └── Total: ~1.5 days

SECOND private markets client (same domain):
  ├── Data Engineer: configure SQL connector           [40 min]
  ├── Domain Expert: NOT NEEDED                        [0]
  │     Definitions already exist from Client 1
  ├── Data Steward: review new column names only       [1 hr]
  │     Platform auto-maps known patterns from Client 1
  └── Total: ~2 hours

TENTH private markets client:
  ├── Data Engineer: configure SQL connector           [40 min]
  ├── Domain Expert: NOT NEEDED                        [0]
  ├── Data Steward: minimal review (most already known)[30 min]
  └── Total: ~1 hour
```

The platform's learning effect: every approved canonical mapping becomes a pattern that applies to all future clients automatically.

---

### Decision Escalation — How Low-Confidence Cases Are Handled

```
New column arrives from client B: "net_irr_pct"

Step 1: Platform runs all signals
  → Confidence: 0.95 → HIGH
  → Decision: AUTO-ACCEPT as NetIRR
  → Data Steward gets FYI notification (no action required)
  → DONE. No human needed.

New column arrives from client D: "fund_perf_rate_adjusted"
  → Confidence: 0.68 → MEDIUM-LOW
  → Decision: DRAFT mapping to "NetIRR" (best guess)
  → Goes to Data Steward review queue
  → Steward sees:
      Column: fund_perf_rate_adjusted
      Table: quarterly_metrics
      Values: 0.156, 0.203
      Best match: NetIRR (0.68 confidence)
      Other options: [GrossIRR 0.61, MOIC 0.22, Other]
  → Steward clicks "NetIRR" or types a different answer
  → Platform learns: "fund_perf_rate_adjusted" pattern → NetIRR
  → Future occurrences auto-mapped

New column arrives from client E: "xyz_calc_v2_final"
  → Confidence: 0.31 → LOW
  → Goes to Data Steward with NO suggestion
  → Steward investigates (looks at values, table context)
  → Steward creates manual mapping or asks Domain Expert
  → OR: Data Engineer adds to abbreviation dictionary
  → Pattern saved for future

New concept needed: client F uses "RVPI" (Residual Value to Paid-In)
  → Platform has never seen RVPI before
  → Flags as "unknown canonical concept"
  → Data Steward escalates to Domain Expert
  → Domain Expert creates new concept definition in YAML
  → PR reviewed → merged → published
  → RVPI is now a known concept for all future clients
```

---

### Practical Scenario: What Happens When Client 4 Joins Tomorrow

```
TIME 0:   Data Engineer provides connection config
          [40 minutes total human work]

TIME 0+5min: Platform connects to SQL Server, lists all tables

TIME 0+30min: Schema extraction complete
              All column names, types, ranges extracted
              Stored in S3

TIME 0+45min: Metadata harvest complete
              AssetMetadata records created for all 8 tables
              Quality scores computed

TIME 1hr:   Canonical mapping runs
              72 columns fingerprinted
              61 columns: confidence ≥ 0.90 → AUTO-MAPPED (no human needed)
              8 columns: confidence 0.75-0.89 → QUEUED for steward review
              3 columns: confidence < 0.75 → QUEUED for manual review

TIME 1hr:   LLM generates candidate definitions for
              unmapped columns (8 candidates sent to steward)

TIME 1hr:   Embeddings generated for all 72 columns and all data rows
              ~10 minutes for embedding pipeline

TIME 1.5hr: OpenSearch index documents created
              All 72 columns and all rows now searchable

TIME 1.5hr: DATA IS NOW SEARCHABLE
              61/72 columns are canonically mapped
              All rows appear in search results
              AI can answer questions about this client's data

TIME +2 days: DATA STEWARD reviews queue (2 hours)
              8 medium-confidence mappings reviewed
              3 manual mappings resolved
              All 72 columns now fully mapped
              Platform learned 11 new patterns

TOTAL HUMAN WORK: Data Engineer 40 min + Data Steward 2 hrs = 2.7 hours
FIRST SEARCHABLE DATA: 1.5 hours after connection config
FULLY CANONICALLY MAPPED: 2-3 days after connection config
```
