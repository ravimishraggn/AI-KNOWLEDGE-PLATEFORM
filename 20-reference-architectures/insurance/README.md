# Reference Architecture: Insurance Knowledge Platform

## Overview

A production reference architecture for deploying the Knowledge Operating Platform in **insurance** organizations. Covers underwriting knowledge, claims intelligence, policy knowledge graphs, actuarial knowledge management, and regulatory compliance.

---

## Target Use Cases

| Use Case | KOP Capability |
|----------|---------------|
| **Underwriting Knowledge Base** | Policy documents → semantic search → underwriter AI |
| **Claims Intelligence** | Claims graph → pattern detection → fraud ontology |
| **Policy Knowledge Graph** | Product → coverage → exclusion → condition graph |
| **Actuarial Knowledge** | Risk models → semantic definition → governed AI |
| **Regulatory Compliance** | Solvency II / IFRS 17 document AI |
| **Agent/Broker Knowledge** | Product knowledge for agent AI assistants |

---

## Industry Standards

### ACORD Data Model
- ACORD XML/JSON standards for insurance data interchange
- Used for: policy, claims, and party data modeling

### XBRL (Solvency II Reporting)
- Regulatory reporting taxonomy
- Used for: Solvency II QRTs, SFCR, RSR

---

## Graph Model (Insurance)

```
(Policy)-[COVERS]->(Risk)
(Policy)-[EXCLUDES]->(Peril)
(Policy)-[ISSUED_BY]->(Insurer)
(Policy)-[HELD_BY]->(Policyholder)
(Claim)-[UNDER]->(Policy)
(Claim)-[CAUSED_BY]->(LossEvent)
(Reinsurance)-[COVERS]->(Policy)
(Risk)-[LOCATED_IN]->(Location)
(Location)-[IN_FLOOD_ZONE]->(FloodZone)
```

---

## Compliance Considerations

- **Solvency II**: Full audit trail for actuarial data and risk models (lineage plane)
- **IFRS 17**: Insurance contract knowledge graph with valuation lineage
- **GDPR**: Customer PII classified RESTRICTED with EU sovereignty
- **Lloyd's Market**: Standardized ACORD taxonomy for market interoperability
