# ADR-004: Plugin Architecture via Python Entry Points

## Status
Accepted

## Date
2025-05-31

## Context

The platform must support extensibility at multiple levels:
- New ingestion connectors (new source systems)
- New graph database backends
- New vector store backends
- New embedding models
- New search engines
- New authentication providers
- New storage backends
- Custom ontology parsers
- Custom enrichment processors

Two main extensibility patterns were evaluated:
1. **Fork-and-modify**: Contributors fork the repo and add their plugin directly
2. **Plugin registry via entry points**: Plugins are separate packages that register themselves with the platform via Python packaging machinery

## Decision

The platform uses **Python Entry Points** (PEP 451) for plugin registration, combined with a **Platform Plugin Registry**:

1. Each pluggable extension point defines an **interface** (ABC) in the relevant plane
2. Plugins are **separate Python packages** that implement the interface
3. Plugins register themselves via `pyproject.toml` entry points under `kop.plugins`
4. The **Plugin Registry** (01-foundation) discovers and loads registered plugins at startup
5. Plugin configuration is schema-validated via Pydantic models
6. Plugins declare their **capability type**, **version**, and **configuration schema**

### Entry Point Convention
```toml
# In a plugin's pyproject.toml
[project.entry-points."kop.connectors"]
s3 = "kop_connector_s3:S3Connector"

[project.entry-points."kop.vector_adapters"]
qdrant = "kop_vector_qdrant:QdrantAdapter"

[project.entry-points."kop.graph_adapters"]
neo4j = "kop_graph_neo4j:Neo4jAdapter"
```

### Plugin Isolation
- Plugins run in the same process but are isolated via dependency injection
- A faulty plugin is caught at registration time or request time — not crashing the whole platform
- Plugins cannot access other tenants' data (tenant context is injected, not accessible globally)

## Consequences

### Positive
- Platform can be extended without forking
- Community can publish plugins to PyPI
- Plugin discovery is automatic (no manual registration in config files)
- Plugin versions are independent of platform versions
- Clear interface contracts prevent plugins from accessing internals

### Negative
- Entry point discovery requires package installation (not just copying files)
- Plugin interface changes require careful versioning
- Plugin quality control requires a community governance model
- Dynamic loading adds startup time for large plugin sets

### Neutral
- Reference implementations for each extension point ship with the platform
- Plugin certification program is a future governance consideration

## Alternatives Considered

### Alternative 1: Configuration-File Plugin Registration
**Why rejected:** Requires manual editing of platform config. More error-prone. Doesn't leverage Python packaging ecosystem.

### Alternative 2: Runtime Plugin Loading from Directory
**Why rejected:** Security risk (arbitrary code execution). No version management. No dependency resolution.

### Alternative 3: Microservice Plugins via HTTP
**Why rejected:** Excessive overhead for simple adapters (an S3 connector doesn't need its own HTTP server). Use MCP for agent-facing extensibility instead.

## References
- [ADR-001](ADR-001-api-first-architecture.md) — APIs define what plugins can offer
- [Foundation Plugin Framework](../../01-foundation/src/knowledge_platform/plugins/)
