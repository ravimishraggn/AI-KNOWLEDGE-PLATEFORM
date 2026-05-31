# Contributing to the Knowledge Operating Platform

Thank you for contributing. This document covers development setup, conventions, and the contribution process.

---

## Development Setup

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git
- Make

### Local Environment

```bash
git clone https://github.com/your-org/knowledge-operating-platform
cd knowledge-operating-platform

# Start backing services
docker-compose up -d postgres redis opensearch kuzu qdrant

# Install foundation in development mode
pip install -e "01-foundation/.[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
make test
```

---

## Repository Conventions

### Branch Naming

```
feature/<plane>/<short-description>
fix/<plane>/<short-description>
docs/<plane>/<short-description>
refactor/<plane>/<short-description>
```

Example: `feature/09-vector-plane/qdrant-adapter`

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(vector-plane): add Qdrant adapter with collection management
fix(governance-plane): correct ABAC policy evaluation order
docs(ontology-plane): add OWL parsing architecture diagram
```

### Pull Requests

- One plane per PR where possible
- All PRs require an architectural summary
- Interfaces must not break without a new ADR
- All new planes require: README, architecture.md, interfaces.md, tests

---

## Plane Development Guide

Each plane follows this structure:

```
<plane>/
├── src/<module>/
│   ├── interfaces/    # Abstract base classes — the public contract
│   ├── models/        # Pydantic models for data structures
│   ├── events/        # Event contracts (CloudEvents compatible)
│   ├── api/           # FastAPI routers
│   └── ...            # Plane-specific subdirectories
├── tests/
│   ├── unit/
│   └── integration/
└── docs/
    ├── README.md
    ├── architecture.md
    ├── interfaces.md
    ├── extension-points.md
    ├── roadmap.md
    ├── tradeoffs.md
    └── future-evolution.md
```

### Interface Contract Rules

1. **Interfaces are sacred** — changing an interface requires an ADR
2. **All adapters implement an interface** — no concrete dependencies between planes
3. **Events are versioned** — event schema changes are backwards compatible for one major version
4. **Plugins register via registry** — no hardcoded implementations

---

## ADR Process

When making a significant architectural decision:

1. Copy `docs/adr/ADR-000-template.md`
2. Number sequentially and name descriptively
3. Status: `Proposed` → `Accepted` → `Deprecated` / `Superseded`
4. Reference the ADR in code comments where the decision is implemented
5. Open a PR — ADRs require team review before acceptance

---

## Testing Requirements

| Test Type | Requirement |
|-----------|-------------|
| Unit tests | All interface methods must have tests |
| Integration tests | All adapters must have integration tests (with real backing services) |
| Contract tests | Cross-plane event contracts must have schema validation tests |
| Performance tests | Search and vector planes must meet latency SLOs |

---

## Code Style

```bash
# Format
ruff format .

# Lint
ruff check .

# Type check
mypy 01-foundation/src

# Run all checks
make lint
```

---

## Questions?

Open a [GitHub Discussion](https://github.com/your-org/knowledge-operating-platform/discussions) for architecture questions.
Open a [GitHub Issue](https://github.com/your-org/knowledge-operating-platform/issues) for bugs.
