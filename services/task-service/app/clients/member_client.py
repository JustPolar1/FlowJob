"""HTTP client for member lookups through the Member Service."""

import os

import httpx


class MemberServiceUnavailableError(Exception):
    """Raised when the Member Service cannot provide a reliable answer."""


def member_exists(member_id: int) -> bool:
    """Return whether a member exists; fail explicitly if lookup is unavailable."""
    base_url = os.getenv("MEMBER_SERVICE_URL", "http://127.0.0.1:8002").rstrip("/")
    try:
        response = httpx.get(f"{base_url}/members/{member_id}", timeout=5.0)
    except httpx.RequestError as error:
        raise MemberServiceUnavailableError(
            "No se pudo consultar el servicio de integrantes."
        ) from error

    if response.status_code == 404:
        return False
    if response.status_code != 200:
        raise MemberServiceUnavailableError(
            f"El servicio de integrantes respondió con HTTP {response.status_code}."
        )
    return True
