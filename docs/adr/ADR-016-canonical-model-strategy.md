# ADR-016: Canonical Model Strategy — Registry-Based Entity Resolution

## Status
Accepted

## Date
2025-05-31

## Context

Enterprise environments have the same real-world entity (e.g., "Goldman Sachs") represented differently in:
- CRM: `goldman_sachs_inc`
- Risk System: `GS_MAIN`
- Bloomberg: `GS US Equity`
- Internal: `Goldman Sachs & Co. LLC`

Without a canonical model layer, the knowledge graph would have 4 disconnected nodes for the same entity. AI systems would fail to recognize that these are the same entity.

## Decision

The Canonical Plane provides a **Registry-Based Entity Resolution** layer:

1. **CanonicalEntityType**: defines entity types (Organisation, Person, Product, Instrument, Location)
2. **CanonicalEntity**: the golden record for an entity — has a platform-wide UUID
3. **EntityMapping**: maps source system identifiers to canonical entity IDs
4. **Resolution Engine**: given an identifier from any system, returns the canonical entity
5. **Synonym Registry**: approved synonyms and aliases for canonical entities
6. **Tenant Extension**: tenants can define their own canonical entity types

### Resolution Strategies
- **Exact match**: identifier → canonical ID (fast lookup)
- **Fuzzy match**: name similarity using embedding similarity
- **Rule-based**: configured regex/pattern rules per source system
- **Graph-based**: use knowledge graph relationships to infer identity

## Consequences

### Positive
- Knowledge graph has one node per real-world entity (not one per source system)
- Cross-system queries become possible
- Entity resolution is a platform service, not duplicated in each consumer

### Negative
- Resolution quality depends on source data quality
- Fuzzy matching introduces false positives — requires human-in-the-loop for ambiguous cases

## References
- [Canonical Plane](../../04-canonical-plane/)
- [ADR-005](ADR-005-knowledge-graph-selection.md) — Knowledge graph stores canonical entities
