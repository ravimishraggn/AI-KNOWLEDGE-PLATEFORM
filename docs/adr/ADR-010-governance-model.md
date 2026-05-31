# ADR-010: Governance Model — RBAC + ABAC with Policy Engine

## Status
Accepted

## Date
2025-05-31

## Context

Enterprise knowledge platforms must enforce access control across multiple dimensions:
- **Role-based**: a Data Analyst can read but not modify ontologies
- **Attribute-based**: a user can only access documents classified at their clearance level
- **Resource-based**: a user can only access their tenant's data
- **Policy-based**: a compliance officer can configure and audit access policies
- **Approval-based**: sensitive operations require approval workflows

Pure RBAC is insufficient: it cannot express "a risk analyst can see PII data only if the data is from their business unit and they have active clearance."

Pure ABAC is too complex: policy language (XACML) is verbose and hard to audit.

## Decision

The Governance Plane implements a **layered governance model**:

1. **Layer 1 — Tenant Isolation** (always enforced, cannot be disabled): Row-level security at the database layer
2. **Layer 2 — RBAC** (role-based access control): Simple, auditable role assignments for common access patterns
3. **Layer 3 — ABAC** (attribute-based): For complex conditions (classification level, business unit, data sovereignty zone)
4. **Layer 4 — Policy Engine**: OPA (Open Policy Agent) for organization-specific policies expressed in Rego
5. **Layer 5 — Approval Workflows**: Temporal-based approval workflows for sensitive operations

### Policy Evaluation Order
```
Request → Tenant Check → Authentication → RBAC Check → ABAC Check → Policy Engine → Decision
```

### Built-in Roles (Platform Level)
```
platform_admin, tenant_admin, data_steward, ontology_manager,
knowledge_engineer, analyst, reader, agent
```

## Consequences

### Positive
- Flexible: RBAC for simple cases, ABAC for complex, OPA for custom policies
- Auditable: every authorization decision is logged
- Separates: authentication (who are you?) from authorization (what can you do?)
- OPA policies are version-controlled and testable

### Negative
- Multiple layers add complexity and latency to authorization
- OPA requires Rego language expertise for custom policies
- Policy conflicts between RBAC and ABAC must be explicitly resolved

## Alternatives Considered

### Alternative 1: RBAC Only
**Why rejected:** Cannot express data-classification-based access control required for banking/healthcare compliance.

### Alternative 2: XACML Policy Engine
**Why rejected:** XACML is verbose and operationally complex. OPA (Rego) is more developer-friendly.

## References
- [ADR-003](ADR-003-multi-tenant-strategy.md) — Tenant isolation (Layer 1)
- [ADR-020](ADR-020-data-sovereignty.md) — Sovereignty uses ABAC (Layer 3)
- [Governance Plane](../../11-governance-plane/)
