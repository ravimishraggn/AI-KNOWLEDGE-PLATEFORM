"""
Platform-wide event contracts.
All events emitted by any plane are defined here as typed models.
Event type naming: kop.{plane}.{entity}.{action}.v{version}
"""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from ..models.base import PlatformEvent


# ── Ingestion Plane Events ──────────────────────────────────────────────────

class DocumentCreatedEvent(PlatformEvent):
    """Emitted when a document is successfully ingested."""
    type: str = "kop.ingestion.document.created.v1"

    class Data:
        document_id: UUID
        source_connector: str
        source_uri: str
        storage_key: str
        content_type: str
        size_bytes: int
        tenant_id: UUID


class IngestionFailedEvent(PlatformEvent):
    """Emitted when an ingestion attempt fails."""
    type: str = "kop.ingestion.document.failed.v1"

    class Data:
        source_uri: str
        connector: str
        error_code: str
        error_message: str
        tenant_id: UUID


# ── Metadata Plane Events ───────────────────────────────────────────────────

class AssetMetadataHarvestedEvent(PlatformEvent):
    """Emitted when metadata is harvested for a knowledge asset."""
    type: str = "kop.metadata.asset.harvested.v1"

    class Data:
        asset_id: UUID
        asset_type: str
        tenant_id: UUID


class AssetClassifiedEvent(PlatformEvent):
    """Emitted when an asset is data-classified."""
    type: str = "kop.metadata.asset.classified.v1"

    class Data:
        asset_id: UUID
        classification: str
        classified_by: str
        tenant_id: UUID


# ── Ontology Plane Events ───────────────────────────────────────────────────

class OntologyPublishedEvent(PlatformEvent):
    """Emitted when an ontology version is published."""
    type: str = "kop.ontology.ontology.published.v1"

    class Data:
        ontology_id: UUID
        ontology_uri: str
        version: str
        tenant_id: UUID


# ── Knowledge Graph Plane Events ────────────────────────────────────────────

class GraphNodeCreatedEvent(PlatformEvent):
    """Emitted when a node is created in the knowledge graph."""
    type: str = "kop.knowledge_graph.node.created.v1"

    class Data:
        node_id: UUID
        node_type: str
        canonical_entity_id: UUID | None
        tenant_id: UUID


class GraphRelationshipCreatedEvent(PlatformEvent):
    """Emitted when a relationship is created in the knowledge graph."""
    type: str = "kop.knowledge_graph.relationship.created.v1"

    class Data:
        relationship_id: UUID
        relationship_type: str
        from_node_id: UUID
        to_node_id: UUID
        tenant_id: UUID


# ── Vector Plane Events ─────────────────────────────────────────────────────

class EmbeddingCreatedEvent(PlatformEvent):
    """Emitted when an embedding is stored in the vector database."""
    type: str = "kop.vector.embedding.created.v1"

    class Data:
        embedding_id: UUID
        asset_id: UUID
        model_id: UUID
        collection_name: str
        dimensions: int
        tenant_id: UUID


# ── Governance Plane Events ─────────────────────────────────────────────────

class PolicyCreatedEvent(PlatformEvent):
    """Emitted when a governance policy is created."""
    type: str = "kop.governance.policy.created.v1"

    class Data:
        policy_id: UUID
        policy_type: str
        tenant_id: UUID


class AccessDeniedEvent(PlatformEvent):
    """Emitted when access to a resource is denied."""
    type: str = "kop.governance.access.denied.v1"

    class Data:
        resource_id: UUID
        resource_type: str
        principal_id: str
        reason: str
        tenant_id: UUID


# ── Lineage Plane Events ────────────────────────────────────────────────────

class LineageRecordedEvent(PlatformEvent):
    """Emitted when a lineage relationship is recorded."""
    type: str = "kop.lineage.transformation.recorded.v1"

    class Data:
        lineage_id: UUID
        source_asset_id: UUID
        target_asset_id: UUID
        transformation_type: str
        actor_id: str
        tenant_id: UUID
