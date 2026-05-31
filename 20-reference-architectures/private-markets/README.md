# Reference Architecture: Private Markets Intelligence Platform

## Overview

A production reference architecture for deploying the Knowledge Operating Platform in **private equity, venture capital, private credit, and real assets** organizations. Covers deal intelligence, portfolio company knowledge, LP/GP relationship graphs, and investment AI.

---

## Target Use Cases

| Use Case | KOP Capability |
|----------|---------------|
| **Deal Intelligence** | CIM/deck ingestion → entity extraction → deal graph |
| **Company Knowledge Graph** | Company → management → investor → sector graph |
| **Portfolio Monitoring AI** | Portfolio company knowledge → AI-powered summaries |
| **LP Relationship Knowledge** | LP → commitment → fund → mandate knowledge graph |
| **Market Intelligence** | News + research → semantic search → analyst AI |
| **Competitive Intelligence** | Company comparison via knowledge graph traversal |

---

## Graph Model (Private Markets)

```
(Company)-[INVESTED_BY]->(InvestmentFirm)
(Company)-[IN_SECTOR]->(Sector)
(Company)-[HAS_MANAGEMENT]->(Person)
(Person)-[WORKED_AT]->(Company)
(InvestmentFirm)-[MANAGES]->(Fund)
(Fund)-[HAS_INVESTOR {commitment_amount}]->(LimitedPartner)
(Deal)-[INVOLVES]->(Company)
(Deal)-[LED_BY]->(InvestmentFirm)
(Company)-[ACQUIRED_BY {date, amount}]->(Company)
(Company)-[SUBSIDIARY_OF]->(Company)
```

---

## Data Sources

| Source | Connector |
|--------|-----------|
| Portfolio company portals | REST API connector |
| CIMs, teaser decks | S3 / SharePoint connector |
| Legal documents (LPAs, PPMs) | S3 connector + document AI |
| News and research | REST API connector (NewsAPI, PitchBook) |
| Bloomberg/Refinitiv | REST API connector |
| Dataroom providers | REST API connector (Intralinks, Ansarada) |

---

## Key Design Considerations

- **Confidentiality**: Deal documents are RESTRICTED by default
- **Carve-outs**: Regulatory carve-outs for certain jurisdictions (SEC, FCA)
- **Data room isolation**: Each deal has a tenant-scoped knowledge space
- **Co-investor graph**: Multi-party graph with access controls per party
