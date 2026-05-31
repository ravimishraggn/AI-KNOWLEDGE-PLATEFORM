# ADR-012: Semantic Layer — Governed Business Glossary

## Status
Accepted

## Date
2025-05-31

## Context

Enterprise AI fails when the same term means different things in different systems. "Customer", "Account", "Risk", "Exposure" — these terms have precise definitions in each business domain that AI models and search systems must understand.

A semantic layer is needed that:
- Defines terms unambiguously for each domain
- Links terms to ontology concepts (OWL)
- Links terms to canonical entity types (Canonical Plane)
- Is version-controlled and governed
- Is consumed by AI systems, search ranking, and knowledge graph labeling

## Decision

The Semantic Plane provides a **governed business glossary** as the primary semantic layer:

1. **GlossaryTerm**: the atomic unit — a defined, owned, versioned business concept
2. Terms are linked to: ontology concepts (OWL URIs), canonical entity types, metadata assets, knowledge graph node types
3. Terms are managed through a **governance workflow** (draft → review → approved → published)
4. **Synonym mapping**: terms have approved synonyms, deprecated synonyms, and cross-domain mappings
5. **Domain scoping**: terms are domain-specific (Finance.Customer ≠ Marketing.Customer)
6. The glossary is tenant-extensible: platform glossary + tenant-specific terms

### GlossaryTerm Schema
```
GlossaryTerm:
  - term_id: UUID
  - tenant_id: UUID (null = platform global)
  - name: str
  - domain: str
  - definition: str
  - examples: list[str]
  - synonyms: list[Synonym]
  - ontology_uri: str (OWL concept URI)
  - canonical_entity_type: str
  - status: TermStatus
  - owner: str
  - approved_by: str
  - version: str
  - effective_date: date
```

## Consequences

### Positive
- AI systems have governed, versioned definitions of business concepts
- Search ranking can be boosted by glossary term matches
- Entity resolution uses glossary synonyms
- Business analysts can author the glossary in natural language

### Negative
- Glossary authoring requires business domain expertise
- Governance workflows add time to concept publication
- Multi-domain synonym management can become complex

## References
- [ADR-008](ADR-008-ontology-management.md) — Glossary terms link to ontology concepts
- [Semantic Plane](../../07-semantic-plane/)
