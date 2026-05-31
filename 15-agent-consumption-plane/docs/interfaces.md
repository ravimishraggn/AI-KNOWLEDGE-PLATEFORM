# Agent Consumption Plane — Interface Contracts

## AgentToolInterface

**Location:** `src/agent_consumption/interfaces/tool.py`

```python
class AgentToolInterface(PluginBase, ABC):
    """
    Interface for knowledge tools exposed to AI agents via MCP.
    Plugin group: kop.agent_tools
    """

    @property
    @abstractmethod
    def tool_name(self) -> str:
        """MCP tool name (e.g., 'kop_search'). Must be globally unique."""
        ...

    @property
    @abstractmethod
    def tool_description(self) -> str:
        """Human-readable description shown to the LLM."""
        ...

    @property
    @abstractmethod
    def input_schema(self) -> dict:
        """JSON Schema for the tool's input parameters."""
        ...

    @property
    @abstractmethod
    def required_roles(self) -> list[str]:
        """Roles required to call this tool."""
        ...

    @abstractmethod
    async def call(
        self,
        arguments: dict,
        principal: Principal,
        tenant_id: UUID,
    ) -> ToolResult:
        """
        Execute the tool with validated arguments.
        Must check authorization before executing.
        Must emit a lineage event on successful retrieval.
        """
        ...
```

---

## MCPServerInterface

**Location:** `src/agent_consumption/interfaces/mcp_server.py`

```python
class MCPServerInterface(ABC):
    """
    MCP server lifecycle management.
    """

    @abstractmethod
    async def list_tools(self, tenant_id: UUID) -> list[ToolDefinition]:
        """Return tools available to the requesting tenant."""
        ...

    @abstractmethod
    async def call_tool(
        self,
        tool_name: str,
        arguments: dict,
        principal: Principal,
        tenant_id: UUID,
    ) -> ToolResult:
        """Route a tool call to the registered tool implementation."""
        ...

    @abstractmethod
    async def list_resources(self, tenant_id: UUID) -> list[ResourceDefinition]:
        """Return MCP resources available to the requesting tenant."""
        ...

    @abstractmethod
    async def read_resource(
        self,
        resource_uri: str,
        principal: Principal,
        tenant_id: UUID,
    ) -> ResourceContent:
        """Read an MCP resource by URI."""
        ...

    @abstractmethod
    async def list_prompts(self, tenant_id: UUID) -> list[PromptDefinition]:
        """Return MCP prompt templates available to the requesting tenant."""
        ...
```

---

## Key Models

```python
class ToolDefinition(BaseModel):
    name: str
    description: str
    input_schema: dict
    required_roles: list[str]

class ToolResult(BaseModel):
    content: list[ToolContent]
    is_error: bool = False

class ToolContent(BaseModel):
    type: str  # "text" | "image" | "resource"
    text: str | None = None
    data: str | None = None  # base64 for images
    mime_type: str | None = None

class ResourceDefinition(BaseModel):
    uri: str
    name: str
    description: str | None = None
    mime_type: str | None = None
```
