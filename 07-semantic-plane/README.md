# 07 — Semantic Plane

The Semantic Plane provides the **governed business glossary** — the platform's semantic layer that defines what business concepts mean, ensures consistency across domains, and grounds AI systems in authoritative definitions.

---

## Responsibilities

- Manage a governed business glossary with full lifecycle (draft → approved)
- Define domain-scoped terms with controlled synonyms and aliases
- Link glossary terms to ontology concepts (Ontology Plane)
- Link glossary terms to canonical entity types (Canonical Plane)
- Provide synonym resolution for search and entity resolution
- Support semantic translation between domain vocabularies
- Enable NLP-friendly concept lookup APIs

---

## Core Concepts

| Concept | Description |
|---------|-------------|
| **GlossaryTerm** | A defined, owned, versioned business concept |
| **Synonym** | An approved alternative name for a term |
| **TermStatus** | draft → review → approved → published → deprecated |
| **Domain** | A business context that scopes a term (Finance, Risk, Marketing) |
| **SemanticMapping** | Cross-domain or cross-system concept alignment |

---

## Glossary Term Lifecycle

```
Draft (by anyone) → Review (by domain steward) → Approved (by governance)
→ Published (platform-wide) → Deprecated (with superseded_by)
```

---

## Integration Points

| Plane | Integration |
|-------|-------------|
| **Ontology Plane** | Terms link to OWL concept URIs |
| **Canonical Plane** | Terms link to canonical entity types |
| **Search Plane** | Term synonyms boost search ranking |
| **AI Consumption** | Terms are used to ground AI responses |
| **Analytics Plane** | Metrics are defined as semantic terms |

---

## Events Emitted

- `kop.semantic.term.published.v1`
- `kop.semantic.term.deprecated.v1`
- `kop.semantic.mapping.created.v1`

---

## Plane Dependencies

- **01-foundation**: auth, event bus
- **05-ontology**: term ↔ concept linking
- **04-canonical**: term ↔ entity type linking
