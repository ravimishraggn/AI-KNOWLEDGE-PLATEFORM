# Governance Plane — Interface Contracts

## AuthorizationInterface

**Location:** `src/governance/interfaces/authorization.py`

```python
class AuthorizationInterface(ABC):
    """
    Primary authorization interface used by all other planes.
    Called on every operation that accesses or modifies knowledge assets.
    """

    @abstractmethod
    async def authorize(
        self,
        principal: Principal,
        action: str,
        resource: Resource,
        context: AuthorizationContext | None = None,
    ) -> AuthorizationDecision:
        """
        Evaluate whether the principal may perform action on resource.
        Returns decision with reason — never raises on denial (returns DENY).
        """
        ...

    @abstractmethod
    async def bulk_authorize(
        self,
        principal: Principal,
        action: str,
        resources: list[Resource],
    ) -> dict[str, AuthorizationDecision]:
        """Evaluate authorization for multiple resources at once."""
        ...

    @abstractmethod
    async def filter_authorized(
        self,
        principal: Principal,
        action: str,
        resources: list[Resource],
    ) -> list[Resource]:
        """Return only the resources the principal is authorized to access."""
        ...
```

---

## PolicyEngineInterface

**Location:** `src/governance/interfaces/policy_engine.py`

```python
class PolicyEngineInterface(PluginBase, ABC):
    """
    Pluggable policy evaluation engine.
    Reference implementation: Open Policy Agent (OPA) with Rego.
    """

    @abstractmethod
    async def evaluate(
        self,
        policy_name: str,
        input_data: dict,
        tenant_id: UUID,
    ) -> PolicyDecision:
        """Evaluate a named policy with the given input. Returns decision + reason."""
        ...

    @abstractmethod
    async def load_policy(
        self,
        policy_name: str,
        policy_content: str,
        tenant_id: UUID,
    ) -> None:
        """Load or update a policy. Content is Rego for OPA implementation."""
        ...

    @abstractmethod
    async def validate_policy(self, policy_content: str) -> PolicyValidationResult:
        """Validate policy syntax and semantics before loading."""
        ...
```

---

## ClassificationInterface

**Location:** `src/governance/interfaces/classification.py`

```python
class ClassificationInterface(ABC):

    @abstractmethod
    async def classify_asset(
        self,
        asset_id: UUID,
        classification: DataClassification,
        classified_by: str,
        tenant_id: UUID,
        justification: str | None = None,
    ) -> ClassificationRecord: ...

    @abstractmethod
    async def get_classification(
        self, asset_id: UUID, tenant_id: UUID
    ) -> ClassificationRecord: ...

    @abstractmethod
    async def auto_classify(
        self, asset_id: UUID, tenant_id: UUID
    ) -> ClassificationSuggestion:
        """Auto-classify based on content analysis heuristics."""
        ...
```

---

## Key Models

```python
class AuthorizationDecision(BaseModel):
    allowed: bool
    reason: str
    policy_evaluated: str | None = None
    conditions: list[str] = []

class DataClassification(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"
    SECRET = "SECRET"
    UNCLASSIFIED = "UNCLASSIFIED"

class Principal(BaseModel):
    user_id: str
    tenant_id: UUID
    roles: list[str]
    attributes: dict = {}  # For ABAC evaluation

class Resource(BaseModel):
    resource_id: UUID
    resource_type: str
    tenant_id: UUID
    classification: DataClassification | None = None
    attributes: dict = {}  # domain, sovereignty_zone, owner, etc.
```
