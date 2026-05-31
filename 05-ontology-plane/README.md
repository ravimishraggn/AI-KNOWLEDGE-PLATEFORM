# 05 — Ontology Plane

The Ontology Plane provides **formal ontology management** for the Knowledge Operating Platform. It is the machine-readable source of truth for what concepts exist, what they mean, and how they relate.

---

## Responsibilities

- Register, validate, version, and publish OWL 2 ontologies
- Register and manage SKOS concept schemes (controlled vocabularies)
- Manage ontology lifecycle: draft → validated → published → deprecated
- Provide APIs for concept lookup, relationship traversal, and reasoning queries
- Support tenant-specific ontology extensions over global platform ontologies
- Align ontology concepts with business glossary terms (Semantic Plane)

---

## Supported Standards

| Standard | Use Case |
|----------|----------|
| **OWL 2 DL** | Formal domain ontologies (banking, healthcare, insurance) |
| **SKOS** | Controlled vocabularies and thesauri |
| **RDF/Turtle** | Canonical serialization format |
| **JSON-LD** | API-friendly ontology exchange |
| **OWL-XML** | Interoperability with Protégé and legacy tools |

---

## Industry Ontology Support (Planned)

| Industry | Ontology |
|----------|---------|
| Banking | FIBO (Financial Industry Business Ontology) |
| Healthcare | SNOMED CT, ICD-11, HL7 FHIR terminology |
| Insurance | ACORD data model ontology |
| General | Schema.org, Dublin Core, PROV-O |

---

## Ontology Lifecycle

```
Draft → [Validation] → Validated → [Review] → Published → [Deprecation] → Deprecated
                                                   ↓
                                            [New Version]
```

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Ontology** | A formal knowledge representation with classes, properties, and axioms |
| **OWLClass** | A concept in the ontology |
| **ObjectProperty** | A typed relationship between classes |
| **DataProperty** | A typed attribute on a class |
| **OntologyVersion** | A point-in-time snapshot with semantic version |
| **OntologyRegistry** | The catalog of all registered ontologies |

---

## Plane Dependencies

- **01-foundation**: auth, event bus, storage
- Consumed by: 07-semantic (glossary ↔ ontology linking), 08-knowledge-graph (node type schemas), 04-canonical (entity type definitions)
