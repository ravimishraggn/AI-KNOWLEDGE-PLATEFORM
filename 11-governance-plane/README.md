# 11 — Governance Plane

The Governance Plane is the platform's **policy engine and access control system**. It enforces who can access what knowledge, under what conditions, and through what approval process. Governance is not a feature — it is a platform primitive present from Day 1.

---

## Responsibilities

- Role-based access control (RBAC): assign and enforce roles
- Attribute-based access control (ABAC): enforce data classification and sovereignty rules
- Policy engine (OPA/Rego): execute organization-specific governance policies
- Approval workflows: multi-step approval for sensitive knowledge operations
- Data classification: classify assets at ingestion and allow re-classification
- Data sovereignty: enforce residency and jurisdiction rules
- Governance audit log: every authorization decision is logged

---

## Governance Layers

| Layer | Mechanism | Override? |
|-------|-----------|-----------|
| **Tenant Isolation** | Row-level security | Never |
| **RBAC** | Role assignments | No (must re-assign role) |
| **ABAC** | Attribute policies | No (must change attribute or policy) |
| **Policy Engine** | OPA Rego policies | By governance admin only |
| **Approval Workflow** | Temporal workflows | After approval |

---

## Built-in Platform Roles

| Role | Permissions |
|------|-------------|
| `platform_admin` | All platform operations |
| `tenant_admin` | All tenant operations |
| `data_steward` | Manage metadata, approve glossary terms |
| `ontology_manager` | Create, version, publish ontologies |
| `knowledge_engineer` | Create/edit knowledge graph nodes and relationships |
| `analyst` | Read access to governed knowledge assets |
| `reader` | Read-only access to published assets |
| `agent` | Tool access for AI agents (scoped to registered tools) |

---

## Data Classification Levels

```
PUBLIC → INTERNAL → CONFIDENTIAL → RESTRICTED → SECRET
```

Each classification level has: access rules, retention policies, sovereignty requirements, and allowed operations.

---

## Events Consumed

- All planes emit events → Governance logs them to audit trail
- `kop.governance.policy.created.v1` → triggers policy re-evaluation

## Events Emitted

- `kop.governance.access.denied.v1`
- `kop.governance.policy.updated.v1`
- `kop.governance.approval.completed.v1`

---

## Plane Dependencies

- **01-foundation**: auth, event bus
- Consumed by: every plane (all operations must be authorized)
