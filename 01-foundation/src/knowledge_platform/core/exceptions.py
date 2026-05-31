"""
Platform exception hierarchy.
All plane-specific exceptions must inherit from KOPException.
FastAPI exception handlers convert these to standardized JSON responses.
"""
from __future__ import annotations

from uuid import UUID


class KOPException(Exception):
    """Root exception for all platform-controlled errors."""
    error_code: str = "PLATFORM_ERROR"
    http_status: int = 500

    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class AuthenticationError(KOPException):
    error_code = "AUTHENTICATION_FAILED"
    http_status = 401


class AuthorizationError(KOPException):
    error_code = "AUTHORIZATION_DENIED"
    http_status = 403


class TenantNotFoundError(KOPException):
    error_code = "TENANT_NOT_FOUND"
    http_status = 404

    def __init__(self, tenant_id: UUID) -> None:
        super().__init__(f"Tenant {tenant_id} not found")


class ResourceNotFoundError(KOPException):
    error_code = "RESOURCE_NOT_FOUND"
    http_status = 404


class ConflictError(KOPException):
    error_code = "RESOURCE_CONFLICT"
    http_status = 409


class ValidationError(KOPException):
    error_code = "VALIDATION_ERROR"
    http_status = 422


class PluginInitializationError(KOPException):
    error_code = "PLUGIN_INIT_FAILED"
    http_status = 500


class PluginNotFoundError(KOPException):
    error_code = "PLUGIN_NOT_FOUND"
    http_status = 500


class SovereigntyViolationError(KOPException):
    error_code = "SOVEREIGNTY_VIOLATION"
    http_status = 403


class ObjectNotFoundError(KOPException):
    error_code = "OBJECT_NOT_FOUND"
    http_status = 404


class PlaneDependencyError(KOPException):
    error_code = "PLANE_DEPENDENCY_UNAVAILABLE"
    http_status = 503
