# 18 — Control Plane

The Control Plane is the **operational command center** of the Knowledge Operating Platform. It manages tenant lifecycle, platform configuration, plugin registry governance, and the governance dashboard.

---

## Responsibilities

- Tenant provisioning, configuration, and deactivation
- Platform-wide configuration management (global + per-tenant overrides)
- Plugin registry governance (approve, disable, version plugins)
- Platform health and registry dashboard
- Feature flag management per tenant
- Plane enable/disable per deployment
- Admin APIs for platform operators

---

## Tenant Lifecycle

```
Provisioning Request
    → Validate tenant config
    → Create PostgreSQL schema
    → Initialize storage bucket
    → Create vector collections
    → Configure sovereignty zone
    → Initialize plugin registry for tenant
    → Emit TenantProvisionedEvent
    → Return TenantRecord
```

## Deactivation

```
Deactivation Request
    → Suspend API access
    → Archive tenant data (per retention policy)
    → Emit TenantDeactivatedEvent
```

---

## Configuration Hierarchy

```
Platform Global Config
    ↓ (tenant can override allowed keys)
Tenant Config
    ↓ (user/agent cannot override)
Request Context
```

---

## Registry Governance

The Control Plane manages:
- Approved connectors (which connectors tenants can use)
- Approved embedding models
- Approved graph and vector backends
- Plugin version pinning per tenant

---

## Platform Dashboard (Planned)

```
/admin/dashboard:
├── Tenant overview (count, status, usage)
├── Plugin registry status
├── Event bus health (stream lag, dead-letter count)
├── Per-plane health status
└── Platform-wide governance audit log
```

---

## Events Emitted

- `kop.control.tenant.provisioned.v1`
- `kop.control.tenant.deactivated.v1`
- `kop.control.plugin.approved.v1`
- `kop.control.config.updated.v1`

---

## Plane Dependencies

- **01-foundation**: all platform primitives
- Manages configuration consumed by all planes
