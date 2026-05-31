# ADR-001: API-First Architecture

## Status
Accepted

## Date
2025-05-31

## Context

The Knowledge Operating Platform must serve a diverse consumer landscape: AI systems, human analysts, agent frameworks, third-party integrations, and internal platform planes. We need a clear contract for how capabilities are exposed and consumed.

Two primary architectural patterns were considered:
- **Library/SDK First**: Core logic as importable Python libraries, with optional HTTP wrappers
- **API First**: HTTP APIs as the primary contract, with SDKs generated from the OpenAPI spec

The platform serves multi-language consumers (Python, TypeScript, Java integrations), must be independently deployable per plane, and must support governance audit trails on all operations.

## Decision

The platform adopts **API First architecture**:

1. Every capability is designed as an HTTP endpoint before any implementation
2. OpenAPI 3.1 specs are generated from FastAPI annotations — not written manually
3. SDKs are generated from OpenAPI specs
4. Planes communicate via their published APIs, not shared libraries
5. All operations are authenticated and observable at the API layer

## Consequences

### Positive
- Language-agnostic: any consumer in any language can use the platform
- Self-documenting: OpenAPI spec is always current
- Independently deployable: planes are microservices with clear boundaries
- Governable: all operations flow through authenticated API calls
- Contract-first: breaking changes require version bumps

### Negative
- Higher latency for same-process operations (vs direct function calls)
- More infrastructure overhead (API gateway, service discovery)
- Inter-plane calls add network hops

### Neutral
- SDK generation requires CI/CD pipeline integration
- Versioning discipline is mandatory from day one

## Alternatives Considered

### Alternative 1: Library-First Architecture
**Description:** Core logic as Python packages. HTTP APIs as optional wrappers.
**Why rejected:** Creates tight coupling between planes. Cross-language consumers require re-implementation. Governance hooks become language-specific.

### Alternative 2: GraphQL API
**Description:** Single GraphQL endpoint for all plane queries.
**Why rejected:** GraphQL federation complexity for 20 planes. OpenAPI tooling ecosystem (code gen, mocking, testing) is more mature. REST is more appropriate for event-driven, resource-oriented operations.

## References
- [Platform Vision](../vision/platform-vision.md)
- [ADR-002](ADR-002-event-driven-architecture.md) — Events complement APIs for async operations
