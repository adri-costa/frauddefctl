from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class BigQueryAdapter:
    project_id: str
    dataset: str | None = None
    table: str | None = None

    def search_assessment_ids(self, assessment_ids: list[str]) -> list[dict[str, Any]]:
        raise NotImplementedError("Implementar consulta ao BigQuery")
