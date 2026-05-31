# ADR-013: Authentication — Pluggable with JWT Default

## Status
Accepted

## Date
2025-05-31

## Context

The platform must support multiple enterprise authentication patterns:
- JWT tokens (stateless, common for API-first architectures)
- OAuth 2.0 / OIDC (enterprise SSO, Azure AD, Okta, Auth0)
- API Keys (service-to-service, agent-to-platform)
- SAML (legacy enterprise)

No single auth mechanism works for all enterprise contexts. The platform must not hard-code any specific auth provider.

## Decision

Authentication is implemented as a **pluggable middleware** with **JWT as the default**:

1. The **AuthInterface** (01-foundation) defines: `validate_token()`, `extract_claims()`, `get_tenant_id()`, `get_user_id()`
2. **JWT with RS256** is the reference implementation (asymmetric keys, stateless verification)
3. **OAuth2/OIDC adapter**: for enterprise SSO via Okta, Azure AD, Auth0
4. **API Key adapter**: for service accounts and agent authentication
5. Auth middleware runs before all route handlers; unauthenticated requests are rejected at the gateway
6. **Tenant context** is extracted from JWT claims and bound to the request

### JWT Claims Contract
```json
{
  "sub": "user_id",
  "tenant_id": "tenant_uuid",
  "roles": ["data_steward", "analyst"],
  "domains": ["banking", "risk"],
  "exp": 1234567890
}
```

## Consequences

### Positive
- Organizations bring their own auth provider (no lock-in)
- JWT is stateless — no shared session store required
- Clean separation: platform handles authorization, adapters handle authentication

### Negative
- JWT token rotation requires careful expiry and refresh token management
- API key management requires a key vault (AWS Secrets Manager, HashiCorp Vault)

## References
- [ADR-010](ADR-010-governance-model.md) — Authorization (what you can do) is separate from authentication (who you are)
- [Foundation Auth](../../01-foundation/src/knowledge_platform/auth/)
