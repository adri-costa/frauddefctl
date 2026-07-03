from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class CloudLoggingAdapter:
    project_id: str

    def search_assessment_ids(self, assessment_ids: list[str]) -> list[dict[str, Any]]:
        raise NotImplementedError("Implementar consulta ao Cloud Logging")
