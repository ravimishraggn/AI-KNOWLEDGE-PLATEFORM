# Semantic Plane — Interface Contracts

## GlossaryInterface

**Location:** `src/semantic/interfaces/glossary.py`

```python
class GlossaryInterface(ABC):

    @abstractmethod
    async def create_term(
        self, term: GlossaryTermCreate, tenant_id: UUID, created_by: str
    ) -> GlossaryTerm:
        """Create a new term in DRAFT status."""
        ...

    @abstractmethod
    async def get_term(self, term_id: UUID, tenant_id: UUID) -> GlossaryTerm: ...

    @abstractmethod
    async def get_term_by_name(
        self, name: str, domain: str, tenant_id: UUID
    ) -> GlossaryTerm: ...

    @abstractmethod
    async def submit_for_review(
        self, term_id: UUID, tenant_id: UUID, submitted_by: str
    ) -> GlossaryTerm: ...

    @abstractmethod
    async def approve_term(
        self, term_id: UUID, tenant_id: UUID, approved_by: str
    ) -> GlossaryTerm: ...

    @abstractmethod
    async def publish_term(
        self, term_id: UUID, tenant_id: UUID
    ) -> GlossaryTerm: ...

    @abstractmethod
    async def deprecate_term(
        self,
        term_id: UUID,
        tenant_id: UUID,
        superseded_by: UUID | None = None,
    ) -> GlossaryTerm: ...

    @abstractmethod
    async def search_terms(
        self,
        query: str,
        tenant_id: UUID,
        domain: str | None = None,
        status: TermStatus | None = None,
    ) -> list[GlossaryTerm]: ...

    @abstractmethod
    async def resolve_synonym(
        self, synonym: str, domain: str, tenant_id: UUID
    ) -> GlossaryTerm | None:
        """Find the canonical term for a given synonym."""
        ...
```

---

## SemanticMappingInterface

**Location:** `src/semantic/interfaces/mapping.py`

```python
class SemanticMappingInterface(ABC):
    """
    Maps concepts between domains, systems, and ontologies.
    """

    @abstractmethod
    async def create_mapping(
        self,
        source_term_id: UUID,
        target_term_id: UUID,
        mapping_type: MappingType,
        tenant_id: UUID,
    ) -> SemanticMapping: ...

    @abstractmethod
    async def get_mappings_for_term(
        self, term_id: UUID, tenant_id: UUID
    ) -> list[SemanticMapping]: ...

    @abstractmethod
    async def translate(
        self,
        term_id: UUID,
        source_domain: str,
        target_domain: str,
        tenant_id: UUID,
    ) -> GlossaryTerm | None:
        """Translate a term from one domain vocabulary to another."""
        ...
```

---

## Key Models

```python
class GlossaryTerm(TenantScopedModel):
    name: str
    domain: str
    definition: str
    examples: list[str] = []
    synonyms: list[Synonym] = []
    ontology_uri: str | None = None        # Links to OWL concept
    canonical_entity_type: str | None = None
    status: TermStatus = TermStatus.DRAFT
    owner: str
    approved_by: str | None = None
    version: str = "1.0"
    effective_date: date | None = None
    tags: list[str] = []

class Synonym(BaseModel):
    value: str
    type: SynonymType  # preferred | acceptable | deprecated | abbreviation
    domain: str | None = None

class MappingType(str, Enum):
    EXACT_MATCH = "exactMatch"          # SKOS exactMatch
    CLOSE_MATCH = "closeMatch"          # SKOS closeMatch
    BROAD_MATCH = "broadMatch"          # SKOS broadMatch
    NARROW_MATCH = "narrowMatch"        # SKOS narrowMatch
    RELATED_MATCH = "relatedMatch"      # SKOS relatedMatch
```
