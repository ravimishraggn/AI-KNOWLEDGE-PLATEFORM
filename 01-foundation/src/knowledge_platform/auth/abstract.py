"""
Authentication provider interface.
Implement this ABC to add a custom authentication mechanism.

Register via entry point:
    [project.entry-points."kop.auth"]
    my_provider = "my_package:MyAuthProvider"
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID


@dataclass
class TokenClaims:
    """Extracted claims from a validated authentication token."""
    subject: str
    tenant_id: UUID
    roles: list[str]
    domains: list[str]
    raw_claims: dict


@dataclass
class TokenPair:
    access_token: str
    refresh_token: str
    expires_in: int


class AuthProvider(ABC):
    """
    Pluggable authentication provider.

    The platform calls validate_token() on every authenticated request.
    All other methods support the token lifecycle.
    """

    @abstractmethod
    async def validate_token(self, token: str) -> TokenClaims:
        """
        Validate the bearer token and return extracted claims.
        Raises AuthenticationError if invalid or expired.
        """
        ...

    @abstractmethod
    async def extract_tenant_id(self, claims: TokenClaims) -> UUID:
        """
        Extract and validate the tenant_id from token claims.
        Raises AuthenticationError if tenant claim is missing or invalid.
        """
        ...

    @abstractmethod
    async def extract_user_id(self, claims: TokenClaims) -> str:
        """Extract the user identifier from token claims."""
        ...

    @abstractmethod
    async def extract_roles(self, claims: TokenClaims) -> list[str]:
        """Extract the list of roles assigned to this principal."""
        ...

    @abstractmethod
    async def refresh_token(self, refresh_token: str) -> TokenPair:
        """
        Exchange a refresh token for a new access+refresh token pair.
        Raises AuthenticationError if refresh token is invalid.
        """
        ...
