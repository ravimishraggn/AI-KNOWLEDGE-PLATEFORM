# Foundation Plane — Extension Points

The Foundation Plane is designed to be extended at every infrastructure boundary. No concrete infrastructure dependency is hardwired.

---

## Extension Point 1: Authentication Provider

**Interface:** `AuthProvider`  
**Plugin Group:** `kop.auth`  
**Config Key:** `KOP_AUTH_PROVIDER`

To provide a custom auth mechanism:

```python
# my_kop_auth_saml/provider.py
from knowledge_platform.auth.abstract import AuthProvider, TokenClaims

class SAMLAuthProvider(AuthProvider):
    async def validate_token(self, token: str) -> TokenClaims:
        # SAML assertion validation
        ...
```

```toml
# pyproject.toml
[project.entry-points."kop.auth"]
saml = "my_kop_auth_saml.provider:SAMLAuthProvider"
```

---

## Extension Point 2: Storage Adapter

**Interface:** `StorageInterface`  
**Plugin Group:** `kop.storage`  
**Config Key:** `KOP_STORAGE_ADAPTER`

Custom storage backends (e.g., Ceph, NetApp, custom enterprise DFS):

```python
from knowledge_platform.storage.abstract import StorageInterface

class CephStorageAdapter(StorageInterface):
    async def put(self, key: str, data: bytes, ...) -> StorageObject:
        ...
```

---

## Extension Point 3: Event Bus Adapter

**Interface:** `EventBusInterface`  
**Plugin Group:** `kop.events`  
**Config Key:** `KOP_EVENT_BUS_ADAPTER`

High-volume deployments can swap Redis Streams for Kafka:

```python
from knowledge_platform.events.bus import EventBusInterface

class KafkaEventBus(EventBusInterface):
    async def publish(self, event: PlatformEvent) -> str:
        ...
```

---

## Extension Point 4: Custom Middleware

Custom middleware can be registered via the plugin system:

```python
from knowledge_platform.plugins.base import PluginBase, PluginCapabilityType

class RateLimitPlugin(PluginBase):
    capability_type = PluginCapabilityType.MIDDLEWARE

    async def initialize(self, config: dict) -> None:
        # Register with FastAPI middleware stack
        ...
```

---

## Extension Point 5: Health Check Contributor

Plugins can register custom health checks that appear in `GET /health/detailed`:

```python
class MyPluginHealthCheck(HealthCheckContributor):
    async def check(self) -> HealthCheckResult:
        return HealthCheckResult(
            name="my_plugin",
            status=HealthStatus.HEALTHY,
            details={"connections": 5}
        )
```

---

## Extension Point 6: Config Schema Extension

Tenants and plugins can extend the configuration schema:

```python
class MyPluginConfig(BasePluginConfig):
    api_key: SecretStr
    endpoint: HttpUrl
    timeout_seconds: int = 30
```

The Foundation validates plugin configs against their declared schema at startup.

---

## What Cannot Be Extended in Foundation

- The tenant isolation model (always enforced, cannot be bypassed)
- The request ID middleware (always present)
- The structured logging format (JSON in production — override in test only)
- The `TenantScopedModel` base fields — they are platform invariants
