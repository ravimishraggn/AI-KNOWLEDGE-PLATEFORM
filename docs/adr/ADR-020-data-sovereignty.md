# ADR-020: Data Sovereignty — Tenant-Bound Classification and Residency

## Status
Accepted

## Date
2025-05-31

## Context

Enterprise customers in banking, healthcare, and insurance operate under strict data residency regulations:
- **GDPR**: EU personal data must remain in the EU
- **CCPA**: California consumer data subject to specific protections
- **HIPAA**: Protected health information (PHI) must be secured with specific controls
- **DORA**: Financial operational resilience requirements in EU
- **Sovereign cloud**: Government customers require data in national cloud regions

The platform must support data sovereignty without requiring separate deployments per jurisdiction.

## Decision

The Governance Plane implements **Tenant-Bound Data Sovereignty**:

1. **Data Classification**: every asset is classified at ingestion (PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED, SECRET)
2. **Sovereignty Zones**: geographic residency rules (EU, US, APAC, UK) bound to data classifications
3. **Tenant Sovereignty Config**: each tenant declares their sovereignty requirements
4. **Storage Routing**: the Storage Abstraction (ADR-014) routes writes to jurisdiction-appropriate buckets
5. **Vector Store Routing**: tenant vectors stored in jurisdiction-appropriate Qdrant clusters
6. **Cross-Zone Query Prevention**: queries that would cross sovereignty boundaries are rejected with a governance error
7. **Sovereignty Audit Log**: all sovereignty-sensitive operations are logged

### Sovereignty Classification Matrix
```
Classification → Sovereignty Zone → Storage Backend → Encryption
RESTRICTED     → EU              → eu-west-1 S3   → Customer-managed KMS
CONFIDENTIAL   → US              → us-east-1 S3   → AWS-managed KMS
```

## Consequences

### Positive
- Regulatory compliance built into the platform, not bolted on
- Automatic storage routing reduces human error
- Audit trail for compliance reporting

### Negative
- Cross-zone analytics are restricted — requires sovereignty-preserving aggregation
- More complex storage routing logic
- Sovereignty zone misclassification is a compliance risk

## References
- [ADR-003](ADR-003-multi-tenant-strategy.md) — Sovereignty builds on tenant isolation
- [ADR-010](ADR-010-governance-model.md) — ABAC enforces sovereignty rules
- [ADR-014](ADR-014-cloud-neutral-storage.md) — Storage routing for sovereignty
- [Governance Plane](../../11-governance-plane/)
