# 15 — Agent Consumption Plane

The Agent Consumption Plane exposes the Knowledge Operating Platform as a **governed, structured tool server for AI agents**. It implements the Model Context Protocol (MCP) as the primary agent interface.

---

## Responsibilities

- Implement an MCP server exposing platform capabilities as agent tools
- Manage the knowledge tool registry (what tools are available to agents)
- Enforce agent-specific access control (scoped, audited tool calls)
- Expose platform knowledge as MCP Resources
- Provide prompt templates for common agentic patterns
- Support custom agent tools as plugins

---

## MCP Server

The Agent Consumption Plane runs an **MCP-compatible server** that any MCP client (Claude, future MCP agents) can connect to:

```
Transport: HTTP + SSE (production)
           stdio (local development)
Auth:      JWT (same as platform API)
Tenant:    Resolved from auth token
```

---

## Knowledge Tools (Planned)

| Tool | Description |
|------|-------------|
| `kop_search` | Search across all knowledge modalities |
| `kop_retrieve` | Retrieve a specific knowledge asset by ID |
| `kop_define` | Look up a business term in the glossary |
| `kop_classify` | Classify text against the ontology |
| `kop_link` | Create a relationship in the knowledge graph |
| `kop_similar` | Find semantically similar assets |
| `kop_lineage` | Get lineage for a knowledge asset |
| `kop_graph_traverse` | Traverse the knowledge graph from a node |
| `kop_context` | Assemble structured context for a query (RAG) |

---

## MCP Resources (Planned)

| Resource | Description |
|----------|-------------|
| `kop://ontology/{id}` | Ontology definition |
| `kop://term/{id}` | Business glossary term |
| `kop://asset/{id}` | Knowledge asset metadata |
| `kop://entity/{id}` | Canonical entity record |

---

## Tool Governance

Every tool call is:
1. **Authenticated**: requires valid JWT with agent role
2. **Authorized**: RBAC/ABAC evaluated for the requested operation
3. **Tenant-scoped**: agent sees only its tenant's knowledge
4. **Logged**: tool call logged to audit trail
5. **Lineage-traced**: retrieval tool calls emit lineage events

---

## Plugin Extension

Custom agent tools can be registered as plugins:
```toml
[project.entry-points."kop.agent_tools"]
my_tool = "my_package:MyAgentTool"
```

---

## Events Emitted

- `kop.agent.tool.called.v1` (feeds audit + lineage)
- `kop.agent.tool.registered.v1`

---

## Plane Dependencies

- **14-ai-consumption**: agent tools delegate to AI consumption APIs
- **10-search**: search tools
- **08-knowledge-graph**: graph traversal tools
- **07-semantic**: define tools
- **11-governance**: tool authorization
