# ADR-008: Ontology Management — OWL/SKOS with Custom Registry

## Status
Accepted

## Date
2025-05-31

## Context

Enterprise knowledge platforms require formal ontological modeling to:
- Define domain concepts and their properties
- Express relationships between concepts (subClassOf, partOf, relatedTo)
- Provide machine-readable definitions for AI systems
- Enable cross-system semantic interoperability

Standards considered:
- **OWL 2** (Web Ontology Language): W3C standard, rich axiomatization, supported by Protégé, heavily used in healthcare (SNOMED, ICD)
- **SKOS** (Simple Knowledge Organization System): W3C standard, simpler, designed for thesauri and controlled vocabularies
- **RDF/RDFS**: Foundation of OWL, more primitive
- **Custom JSON schema**: Simple but non-interoperable with the semantic web ecosystem

## Decision

The Ontology Plane supports **OWL 2** for formal ontologies and **SKOS** for controlled vocabularies, with a **Custom Ontology Registry** managing lifecycle:

1. **OWL 2** is the primary format for domain ontologies (banking, healthcare, insurance)
2. **SKOS** is used for taxonomies and controlled vocabularies (integrated with Taxonomy Plane)
3. The **Ontology Registry** manages: registration, versioning, validation, and publication
4. Ontologies are stored in **Turtle (.ttl)** format as the canonical serialization
5. Ontologies are **tenant-scoped**: global platform ontologies + tenant-specific extensions
6. **Ontology versioning** follows semantic versioning with migration paths between versions
7. The **Semantic Plane** uses the Ontology Registry as its source of truth for concept definitions

### Ontology Lifecycle
```
Draft → Validated → Published → Deprecated → Superseded
```

### Industry Ontology Support (Planned)
- **Banking**: FIBO (Financial Industry Business Ontology)
- **Healthcare**: SNOMED CT, ICD-11, HL7 FHIR terminology
- **Insurance**: ACORD data standards
- **General**: Schema.org, Dublin Core

## Consequences

### Positive
- W3C standards compliance enables interoperability with external systems
- OWL reasoners can be used for automated classification
- Protégé and other OWL tools work with platform ontologies
- SKOS integration with Taxonomy Plane creates a unified semantic layer

### Negative
- OWL complexity is a barrier to entry for non-ontologists
- Reasoning on large OWL ontologies is computationally expensive
- Custom ontology validation requires ontology-specific expertise

### Neutral
- Platform provides simplified ontology authoring APIs (not raw OWL required)
- Ontology editors (Protégé, WebVOWL) can be integrated as external tools

## Alternatives Considered

### Alternative 1: Custom JSON-LD Schema Only
**Why rejected:** Not interoperable with semantic web tooling. Defeats the purpose of semantic modeling.

### Alternative 2: SKOS Only
**Why rejected:** SKOS cannot express rich axioms (cardinality, property restrictions). Insufficient for formal domain ontologies.

## References
- [Ontology Plane](../../05-ontology-plane/)
- [Taxonomy Plane](../../06-taxonomy-plane/)
- [ADR-012](ADR-012-semantic-layer.md) — Semantic layer uses ontologies
