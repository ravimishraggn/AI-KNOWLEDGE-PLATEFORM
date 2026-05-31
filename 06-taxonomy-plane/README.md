# 06 — Taxonomy Plane

The Taxonomy Plane manages **hierarchical classification systems** — the organizational structures that group knowledge assets, entities, and concepts into meaningful categories.

---

## Responsibilities

- Manage hierarchical taxonomies (parent-child category trees)
- Manage controlled vocabularies and tag registries
- Support SKOS concept schemes (aligned with Ontology Plane)
- Provide classification APIs for tagging knowledge assets
- Enable faceted search filtering via taxonomy terms
- Support multi-lingual taxonomy labels

---

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Taxonomy** | A named hierarchical classification system |
| **TaxonomyNode** | A node in the hierarchy (category, term, code) |
| **ControlledVocabulary** | A flat list of approved terms |
| **ClassificationTag** | A taxonomy term applied to a knowledge asset |

---

## Example Taxonomies

### Banking Taxonomy
```
Banking Products
├── Lending
│   ├── Corporate Loans
│   │   ├── Revolving Credit Facilities
│   │   └── Term Loans
│   └── Retail Loans
│       ├── Mortgages
│       └── Personal Loans
└── Investments
    ├── Fixed Income
    └── Equities
```

### Document Type Taxonomy
```
Document Types
├── Regulatory
│   ├── Regulation
│   ├── Guidance
│   └── Q&A
├── Internal
│   ├── Policy
│   └── Procedure
└── Research
    ├── Analysis
    └── Report
```

---

## Integration with Ontology Plane

Each taxonomy node can be linked to an OWL class (SKOS narrower/broader relationships). This provides formal semantics behind the classification hierarchy.

---

## Events Emitted

- `kop.taxonomy.node.created.v1`
- `kop.taxonomy.classification.applied.v1`

---

## Plane Dependencies

- **01-foundation**: auth, event bus
- **05-ontology**: SKOS alignment
- Consumed by: 10-search (faceted filtering), 03-metadata (asset classification)
