# ADR-017: Agent Protocol — MCP as Primary Agent Interface

## Status
Accepted

## Date
2025-05-31

## Context

AI agents (Claude, GPT, custom agents) need to interact with the knowledge platform as a structured tool provider. Two main patterns:
1. **Custom REST APIs per agent**: each agent integration is bespoke
2. **Model Context Protocol (MCP)**: emerging standard for agent-tool communication

MCP (introduced by Anthropic in 2024) provides a standardized protocol for: tool discovery, tool calling, resource access, and prompt templates — enabling any MCP-compatible agent to use the platform without custom integration.

## Decision

The Agent Consumption Plane exposes an **MCP Server** as the primary agent interface:

1. Platform capabilities are exposed as **MCP Tools** (search, retrieve, classify, link, govern)
2. Knowledge assets are exposed as **MCP Resources** (documents, ontologies, glossary terms)
3. Prompt templates for common agentic patterns are **MCP Prompts**
4. The MCP server is **tenant-aware** and **governance-enforced**
5. MCP transport: **HTTP+SSE** (primary), **stdio** (local development)

### Platform MCP Tools (planned)
```
kop_search        — Search across all knowledge modalities
kop_retrieve      — Retrieve a specific knowledge asset
kop_classify      — Classify an entity against the ontology
kop_link          — Create a relationship in the knowledge graph
kop_define        — Look up a business term in the glossary
kop_lineage       — Get lineage for a knowledge asset
kop_similar       — Find semantically similar assets
```

## Consequences

### Positive
- Any MCP-compatible agent (Claude, future standards adopters) works immediately
- No bespoke integration per agent type
- Tool governance is centralized in the Agent Consumption Plane
- Tool versioning follows MCP spec

### Negative
- MCP is a newer standard — tooling ecosystem is still maturing
- MCP server adds another service to operate

## References
- [Agent Consumption Plane](../../15-agent-consumption-plane/)
- [ADR-001](ADR-001-api-first-architecture.md) — APIs underpin MCP tools
