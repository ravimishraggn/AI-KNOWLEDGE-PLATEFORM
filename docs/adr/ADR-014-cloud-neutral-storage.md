# ADR-014: Cloud-Neutral Storage Abstraction

## Status
Accepted

## Date
2025-05-31

## Context

The platform ingests and stores knowledge assets from/to cloud object storage. Different organizations use different providers (AWS S3, Azure Blob, GCP GCS) or on-premise solutions (MinIO, Ceph).

Hard-coding AWS S3 APIs would violate the Vendor Neutral principle (ADR-000 equivalent).

## Decision

The Foundation provides a **StorageInterface** that abstracts all object storage operations:

1. **StorageInterface** defines: `put()`, `get()`, `delete()`, `list()`, `exists()`, `get_url()`
2. **S3Adapter**: AWS S3 (primary reference implementation)
3. **AzureBlobAdapter**: Azure Blob Storage
4. **GCSAdapter**: Google Cloud Storage
5. **MinIOAdapter**: On-premise / self-hosted (MinIO is S3-compatible)
6. **LocalFileAdapter**: Development and testing

Storage configuration is per-tenant: a tenant can use a different storage backend than the platform default.

## Consequences

### Positive
- Organizations bring their own cloud storage (no AWS lock-in)
- On-premise deployments use MinIO (S3-compatible)
- Per-tenant storage routing enables data sovereignty (store EU tenant data in EU S3 bucket)

### Negative
- Abstraction has performance cost for high-throughput ingestion
- Some cloud-specific features (S3 Intelligent-Tiering, Lifecycle policies) are not exposed through the interface

## References
- [ADR-003](ADR-003-multi-tenant-strategy.md) — Per-tenant storage routing
- [Foundation Storage](../../01-foundation/src/knowledge_platform/storage/)
