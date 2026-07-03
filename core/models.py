from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class ExecutionMode(str, Enum):
    INTERACTIVE = "interactive"
    PIPELINE = "pipeline"


class RiskStatus(str, Enum):
    SAFE = "SAFE"
    RISK = "RISK"
    UNKNOWN = "UNKNOWN"


class OutputFormat(str, Enum):
    TABLE = "table"
    CSV = "csv"
    JSON = "json"
    MARKDOWN = "markdown"


class ProjectConfig(BaseModel):
    project_id: str
    alias: str | None = None
    project_number: str | None = None
    environment: str | None = None
    owner_team: str | None = None
    enabled: bool = True


class DefaultsConfig(BaseModel):
    score_safe_threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    obsolete_days_without_traffic: int = Field(default=90, ge=1)
    output_dir: Path = Path("reports")
    export_formats: list[str] = Field(default_factory=lambda: ["csv", "json", "markdown"])
    csv_separator: str = ";"
    timezone: str = "America/Sao_Paulo"


class ReportsConfig(BaseModel):
    mask_sensitive_data: bool = True
    include_timestamp_in_filename: bool = True
    generate_summary: bool = True
    generate_evidence_package: bool = True


class FraudDefCtlConfig(BaseModel):
    projects: list[ProjectConfig]
    defaults: DefaultsConfig = Field(default_factory=DefaultsConfig)
    reports: ReportsConfig = Field(default_factory=ReportsConfig)
    labels_standard: dict[str, Any] = Field(default_factory=dict)


class AssessmentRecord(BaseModel):
    assessment_id: str
    project_id: str | None = None
    site_key_id: str | None = None
    display_name: str | None = None
    timestamp: str | None = None
    action_expected: str | None = None
    action_returned: str | None = None
    hostname: str | None = None
    token_valid: bool | None = None
    invalid_reason: str | None = None
    score_decimal: float | None = Field(default=None, ge=0.0, le=1.0)
    reasons: list[str] = Field(default_factory=list)
    challenge_result: str | None = None
    application_decision: str | None = None
    log_found: bool | None = None
    annotation_found: bool | None = None


class AssessmentVerdict(BaseModel):
    assessment_id: str
    score_decimal: float | None
    score_bucket: int | None
    risk_status: RiskStatus
    threshold: float
