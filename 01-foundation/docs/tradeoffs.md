# Foundation Plane — Architectural Tradeoffs

## Tradeoff 1: Python vs Go for the API Framework

**Chose:** Python + FastAPI  
**Alternative rejected:** Go + Gin or Echo

**Why:**
- Python's ML/AI ecosystem is unmatched — embedding models, graph libraries, NLP tooling
- FastAPI's Pydantic-based schema validation maps directly to the platform's contract-first design
- Developer pool for enterprise Python is larger than Go in the knowledge/AI domain

**Cost:**
- Python GIL limits CPU-bound concurrency (not material — the platform is I/O bound)
- Python startup time is slower than Go (mitigated with warm Kubernetes pods)

---

## Tradeoff 2: Plugin System via Entry Points vs Configuration Files

**Chose:** Python entry points (packaging-based plugin discovery)  
**Alternative rejected:** YAML/JSON plugin registration config files

**Why:**
- Entry points integrate with the Python packaging ecosystem (pip install → auto-discovery)
- Version management is handled by pip dependency resolution
- No "plugin config drift" (config file says plugin exists, plugin package not installed)

**Cost:**
- Plugins must be installed as packages — cannot "drop a file" into a folder
- Requires understanding of Python packaging for plugin authors

---

## Tradeoff 3: Redis Streams as Default Event Bus vs Kafka

**Chose:** Redis Streams (default), Kafka (adapter)  
**Alternative rejected:** Kafka as default

**Why:**
- Redis Streams requires zero additional infrastructure (Redis is already required for caching)
- Kafka adds significant operational complexity (ZooKeeper/KRaft, topic management, schema registry)
- 90% of KOP deployments won't need Kafka's throughput (10M+ msg/sec)

**Cost:**
- Redis Streams has lower durability guarantees than Kafka (mitigated with AOF persistence)
- Redis Streams is single-node by default (Redis Cluster for HA)
- Migration from Redis Streams to Kafka requires consumer group migration

---

## Tradeoff 4: Synchronous Config vs Feature Flags Service

**Chose:** Pydantic Settings from environment variables (12-Factor App)  
**Alternative rejected:** Feature flag service (LaunchDarkly, Flagsmith) from day one

**Why:**
- Environment variables are universally supported (Docker, Kubernetes, .env)
- No additional service dependency in the foundation
- Feature flags service can be added as a plugin when needed

**Cost:**
- Config changes require pod restart (no hot-reload)
- Tenant-specific feature overrides require the Control Plane

---

## Tradeoff 5: Single Process vs Microservices per Plane

**Chose:** Planes as modules in one deployable (default), with option to split  
**Alternative rejected:** Every plane as a separate microservice from day one

**Why:**
- Single-process deployment massively reduces operational complexity for small teams
- Local development with `docker-compose up` is much simpler
- Planes communicate via Python function calls (no network hop) in single-process mode
- Can be split into microservices when scale demands it

**Cost:**
- Single process has shared failure domain
- Cannot scale planes independently in single-process mode
- Requires discipline to maintain plane boundaries even in single-process
