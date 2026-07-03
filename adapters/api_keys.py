from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ApiKeysAdapter:
    """Adapter para Google Cloud API Keys API."""

    project_id: str

    def list_api_keys(self) -> list[dict[str, Any]]:
        raise NotImplementedError("Implementar com google-cloud-api-keys")

    def create_api_key(self, payload: dict[str, Any], *, dry_run: bool = True) -> dict[str, Any]:
        if dry_run:
            return {"dry_run": True, "payload": payload}
        raise NotImplementedError("Implementar criação de API key")

    def update_restrictions(self, key_id: str, restrictions: dict[str, Any], *, dry_run: bool = True) -> dict[str, Any]:
        if dry_run:
            return {"dry_run": True, "key_id": key_id, "restrictions": restrictions}
        raise NotImplementedError("Implementar update de restrições")
