# Ontology Plane — Interface Contracts

## OntologyRegistryInterface

**Location:** `src/ontology/interfaces/registry.py`

```python
class OntologyRegistryInterface(ABC):

    @abstractmethod
    async def register(
        self,
        ontology: OntologyUpload,
        tenant_id: UUID,
    ) -> OntologyRecord:
        """Register a new ontology or a new version of an existing ontology."""
        ...

    @abstractmethod
    async def get(self, ontology_id: UUID, tenant_id: UUID) -> OntologyRecord: ...

    @abstractmethod
    async def get_by_uri(self, uri: str, tenant_id: UUID) -> OntologyRecord: ...

    @abstractmethod
    async def publish(self, ontology_id: UUID, tenant_id: UUID) -> OntologyRecord:
        """Promote an ontology from Validated to Published status."""
        ...

    @abstractmethod
    async def deprecate(
        self,
        ontology_id: UUID,
        tenant_id: UUID,
        superseded_by: UUID | None = None,
    ) -> OntologyRecord: ...

    @abstractmethod
    async def list_ontologies(
        self, tenant_id: UUID, filters: OntologyFilters | None = None
    ) -> PaginatedResponse[OntologyRecord]: ...

    @abstractmethod
    async def get_concept(self, concept_uri: str, tenant_id: UUID) -> OWLClass: ...

    @abstractmethod
    async def search_concepts(
        self, query: str, tenant_id: UUID, limit: int = 20
    ) -> list[OWLClass]: ...
```

---

## OntologyParserInterface

**Location:** `src/ontology/interfaces/parser.py`

```python
class OntologyParserInterface(PluginBase, ABC):
    """
    Parses an ontology file in a specific format into platform's internal model.
    Implementations: TurtleParser, OWLXMLParser, JSONLDParser, RDFXMLParser
    """

    @abstractmethod
    def supported_formats(self) -> list[str]:
        """Return list of supported MIME types or file extensions."""
        ...

    @abstractmethod
    async def parse(self, content: bytes, format: str) -> ParsedOntology:
        """Parse ontology content and return structured internal representation."""
        ...

    @abstractmethod
    async def validate(self, parsed: ParsedOntology) -> OntologyValidationResult:
        """Validate OWL consistency and completeness."""
        ...
```

---

## Key Models

```python
class OntologyRecord(TenantScopedModel):
    name: str
    uri: str               # Canonical ontology URI (IRI)
    version: str           # Semantic version: "1.0.0"
    status: OntologyStatus
    format: OntologyFormat
    storage_key: str       # Where the raw ontology file is stored
    description: str | None
    domain: str | None
    class_count: int = 0
    property_count: int = 0
    is_global: bool = False   # True = platform-wide, False = tenant-specific

class OWLClass(BaseModel):
    uri: str
    label: str
    comment: str | None
    super_classes: list[str]
    sub_classes: list[str]
    equivalent_classes: list[str]
    ontology_id: UUID
    tenant_id: UUID

class OntologyStatus(str, Enum):
    DRAFT = "draft"
    VALIDATED = "validated"
    PUBLISHED = "published"
    DEPRECATED = "deprecated"
```
