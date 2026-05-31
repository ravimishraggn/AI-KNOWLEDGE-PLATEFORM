# 19 — Developer Experience

The Developer Experience plane provides the tooling that makes the Knowledge Operating Platform **accessible, learnable, and productive** for engineers building on top of it.

---

## Deliverables

### `kop` CLI

```bash
# Authentication
kop login --platform https://kop.example.com

# Tenant management
kop tenant list
kop tenant create --name "acme-banking" --domain "banking"

# Ingestion
kop ingest s3 s3://my-bucket/docs/ --tenant acme-banking

# Search
kop search "credit risk exposure Goldman Sachs" --tenant acme-banking

# Ontology
kop ontology import my-ontology.ttl --tenant acme-banking
kop ontology publish <ontology-id>

# Glossary
kop term create --name "Customer" --domain "banking" --definition "..."

# Knowledge Graph
kop graph query "MATCH (o:Organisation) RETURN o LIMIT 10"
```

### Python SDK

Generated from the platform's OpenAPI spec:

```python
from kop_sdk import KOPClient

client = KOPClient(
    base_url="https://kop.example.com",
    token="your-jwt-token",
    tenant_id="acme-banking"
)

# Search
results = await client.search.query(
    query="credit risk exposure",
    strategies=["hybrid"],
    limit=10
)

# Ontology
ontology = await client.ontology.get_by_uri("https://spec.edmcouncil.org/fibo/")

# RAG Context
context = await client.ai.get_context(
    query="What is our counterparty risk exposure?",
    max_tokens=4000
)
```

### TypeScript SDK

```typescript
import { KOPClient } from '@kop/sdk';

const client = new KOPClient({
  baseUrl: 'https://kop.example.com',
  token: 'your-jwt-token',
  tenantId: 'acme-banking'
});

const results = await client.search.query({
  query: 'credit risk exposure',
  strategies: ['hybrid'],
  limit: 10
});
```

---

## Examples

| Example | Location |
|---------|---------|
| Banking Knowledge Graph | `examples/banking/` |
| Healthcare Ontology Import | `examples/healthcare/` |
| RAG Pipeline | `examples/rag-pipeline/` |

---

## Templates

| Template | Location |
|----------|---------|
| New Connector | `templates/connector/` |
| New Ontology | `templates/ontology/` |
| New Agent Tool | `templates/agent/` |

---

## Tutorials

- Getting Started: First Knowledge Asset
- Importing an OWL Ontology
- Building a RAG Pipeline
- Connecting an AI Agent via MCP
- Multi-Tenant Setup
