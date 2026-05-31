# ADR-009: Metadata Strategy — Unified Technical and Business Metadata

## Status
Accepted

## Date
2025-05-31

## Context

Enterprise metadata exists in two disconnected worlds:
- **Technical metadata**: table schemas, column types, row counts, data quality scores — managed by data engineers
- **Business metadata**: definitions, owners, stewards, policies, classifications — managed by data governance teams

Most tools serve one or the other. This disconnect causes: AI hallucinations (no business context), governance failures (no technical context), and poor data quality (no unified quality signal).

## Decision

The Metadata Plane provides **unified technical and business metadata** for every knowledge asset:

1. **Asset = any discoverable knowledge object**: document, dataset, table, column, API endpoint, ontology concept, knowledge graph node, vector collection, embedding model
2. Every asset has a **Unified Metadata Record** with both technical and business dimensions
3. Metadata is **automatically harvested** from technical sources (schema introspection, file analysis, API crawling)
4. Business metadata is managed through **governed workflows** (not free-form editing)
5. Metadata records are **event-sourced** — full history of every metadata change
6. **Quality scores** are computed automatically and displayed alongside metadata
7. The Metadata Plane emits events consumed by: Search (for discovery), Governance (for policy enforcement), Lineage (for provenance)

### Unified Metadata Record Schema
```
AssetMetadata:
  - asset_id: UUID
  - tenant_id: UUID
  - asset_type: [document | dataset | table | column | concept | node | ...]
  - technical:
      - source_system: str
      - schema_info: dict
      - format: str
      - size: int
      - quality_score: float
  - business:
      - name: str
      - description: str
      - owner: str
      - steward: str
      - domain: str
      - classification: DataClassification
      - tags: list[str]
      - glossary_terms: list[GlossaryTermRef]
  - governance:
      - policy_ids: list[UUID]
      - sovereignty_zone: str
      - retention_policy: str
  - lineage:
      - created_from: list[AssetRef]
      - feeds_into: list[AssetRef]
  - timestamps:
      - created_at, updated_at, harvested_at
```

## Consequences

### Positive
- Single place to discover everything about an asset
- AI systems can access business context alongside technical details
- Governance policies are metadata-driven — no hardcoding
- Automated harvesting reduces manual metadata burden

### Negative
- Unified record increases complexity of the metadata model
- Harvesting from heterogeneous systems requires plane-specific connectors
- Quality scores must be carefully defined to be meaningful

## Alternatives Considered

### Alternative 1: Separate Business and Technical Metadata Catalogs
**Why rejected:** Creates the exact disconnect we're trying to solve. Forces consumers to join across two systems.

## References
- [Metadata Plane](../../03-metadata-plane/)
- [Governance Plane](../../11-governance-plane/) — Consumes metadata for policy enforcement
