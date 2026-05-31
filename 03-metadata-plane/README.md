# 03 — Metadata Plane

The Metadata Plane is the platform's **knowledge catalog** — a unified registry of every knowledge asset with its technical and business metadata.

---

## Responsibilities

- Automatically harvest technical metadata on ingestion events
- Manage business metadata through governed authoring workflows
- Maintain the unified metadata record (technical + business + governance)
- Compute data quality scores
- Expose discovery APIs for search and governance
- Emit metadata events consumed by search and governance planes

---

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Asset** | Any discoverable knowledge object (document, table, concept, node, embedding) |
| **AssetMetadata** | Unified metadata record: technical + business + governance dimensions |
| **MetadataHarvester** | Plugin that extracts metadata from a specific asset type |
| **MetadataCatalog** | The queryable registry of all asset metadata records |
| **QualityScore** | Computed score across: completeness, accuracy, timeliness, consistency |

---

## Metadata Dimensions

```
AssetMetadata
├── Technical Metadata (auto-harvested)
│   ├── Source system, format, size, schema
│   ├── Data quality metrics
│   └── Technical statistics
├── Business Metadata (human-authored)
│   ├── Name, description, owner, steward
│   ├── Domain, business glossary terms
│   └── Tags, business context
└── Governance Metadata (system-managed)
    ├── Classification, policy IDs
    ├── Sovereignty zone
    ├── Retention policy
    └── Access control rules
```

---

## Events Consumed

- `kop.ingestion.document.created.v1` → triggers metadata harvest

## Events Emitted

- `kop.metadata.asset.harvested.v1`
- `kop.metadata.asset.classified.v1`
- `kop.metadata.asset.updated.v1`

---

## Plane Dependencies

- **01-foundation**: event bus (consumer), storage, auth
- Consumes events from: 02-ingestion
- Emits events consumed by: 10-search, 11-governance, 12-lineage
