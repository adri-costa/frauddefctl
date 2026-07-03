from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class RecaptchaAdapter:
    """Adapter SDK/API-first para reCAPTCHA Enterprise.

    Implementação real será plugada na próxima fase com google-cloud-recaptcha-enterprise.
    Mantemos a interface estável para a UI e para o modo pipeline.
    """

    project_id: str

    def list_keys(self) -> list[dict[str, Any]]:
        raise NotImplementedError("Implementar com google-cloud-recaptcha-enterprise")

    def get_key_metrics(self, site_key_id: str) -> dict[str, Any]:
        raise NotImplementedError("Implementar GetMetrics")

    def list_ip_overrides(self, site_key_id: str) -> list[dict[str, Any]]:
        raise NotImplementedError("Implementar listIpOverrides")

    def create_key(self, payload: dict[str, Any], *, dry_run: bool = True) -> dict[str, Any]:
        if dry_run:
            return {"dry_run": True, "payload": payload}
        raise NotImplementedError("Implementar criação de chave")

    def delete_key(self, site_key_id: str, *, dry_run: bool = True) -> dict[str, Any]:
        if dry_run:
            return {"dry_run": True, "site_key_id": site_key_id}
        raise NotImplementedError("Implementar remoção de chave")
