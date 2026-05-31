"""
Plugin base class and capability type registry.
Every extensible component in the platform is a plugin.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class PluginCapabilityType(str, Enum):
    """All plugin capability types recognized by the platform."""
    CONNECTOR = "connector"
    GRAPH_ADAPTER = "graph_adapter"
    VECTOR_ADAPTER = "vector_adapter"
    SEARCH_ENGINE = "search_engine"
    EMBEDDING_MODEL = "embedding_model"
    AUTH_PROVIDER = "auth_provider"
    STORAGE_ADAPTER = "storage_adapter"
    EVENT_BUS = "event_bus"
    ONTOLOGY_PARSER = "ontology_parser"
    ENRICHER = "enricher"
    CLASSIFIER = "classifier"
    MIDDLEWARE = "middleware"
    RERANKER = "reranker"


class PluginHealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


@dataclass
class PluginHealth:
    status: PluginHealthStatus
    message: str | None = None
    details: dict | None = None


class PluginBase(ABC):
    """
    Base class for all platform plugins.
    Plugins are discovered via Python entry points and managed by PluginRegistry.
    """

    @property
    @abstractmethod
    def plugin_id(self) -> str:
        """Unique identifier (e.g., 's3', 'neo4j', 'qdrant')."""
        ...

    @property
    @abstractmethod
    def plugin_version(self) -> str:
        """Semantic version string (e.g., '1.0.0')."""
        ...

    @property
    @abstractmethod
    def capability_type(self) -> PluginCapabilityType:
        """The capability type this plugin provides."""
        ...

    @abstractmethod
    async def initialize(self, config: dict) -> None:
        """
        Initialize with validated configuration.
        Raises PluginInitializationError on failure.
        Called once at platform startup.
        """
        ...

    @abstractmethod
    async def health_check(self) -> PluginHealth:
        """Return current health status. Called by /health/detailed."""
        ...

    @abstractmethod
    async def shutdown(self) -> None:
        """Gracefully release resources. Called at platform shutdown."""
        ...
