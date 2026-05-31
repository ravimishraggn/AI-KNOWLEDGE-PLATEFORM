# 04 — Canonical Plane

The Canonical Plane provides **cross-system entity resolution** — the capability to recognize that `GS_MAIN`, `goldman_sachs_inc`, and `Goldman Sachs & Co.` all refer to the same real-world legal entity. It maintains the golden record for every entity in the platform.

---

## Responsibilities

- Define and manage canonical entity types (Organisation, Person, Product, Instrument, Location)
- Resolve source-system identifiers to canonical entity IDs
- Maintain synonym and alias registries
- Enable cross-system entity matching (exact, fuzzy, graph-based)
- Manage cross-system identifier mappings (Bloomberg ID, LEI, ISIN, etc.)
- Provide canonical entity APIs for knowledge graph node creation

---

## Supported Entity Types

| Entity Type | Identifiers |
|-------------|-------------|
| **Organisation** | LEI, DUNS, Tax ID, Bloomberg, Refinitiv |
| **Person** | Internal ID, Employee ID |
| **FinancialInstrument** | ISIN, CUSIP, SEDOL, Bloomberg Ticker |
| **Location** | ISO 3166, Geonames ID |
| **Product** | SKU, Product ID, EAN |
| **Regulation** | Regulation URI, Official Journal ref |

---

## Resolution Strategies

| Strategy | When Used | Accuracy |
|----------|-----------|---------|
| **Exact match** | Known identifiers (LEI, ISIN) | 100% |
| **Rule-based** | Configured regex patterns | High |
| **Fuzzy name match** | Name similarity (Levenshtein, Jaro-Winkler) | Medium |
| **Embedding similarity** | Semantic entity matching via vector | Medium |
| **Graph-based** | Use relationship context (same address, same director) | High |
| **Human review** | Ambiguous cases requiring manual confirmation | 100% |

---

## Events Emitted

- `kop.canonical.entity.created.v1`
- `kop.canonical.mapping.added.v1`
- `kop.canonical.entity.merged.v1`

---

## Plane Dependencies

- **01-foundation**: auth, event bus
- **05-ontology**: entity types derived from ontology classes
- **09-vector**: fuzzy matching via vector similarity
- Consumed by: 08-knowledge-graph (node creation), 07-semantic (term linking)
