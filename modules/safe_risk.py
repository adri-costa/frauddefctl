from __future__ import annotations

from collections import Counter
from typing import Iterable

from frauddefctl.core.models import AssessmentRecord, RiskStatus
from frauddefctl.core.risk import classify_assessment, score_to_bucket


def summarize_safe_risk(records: Iterable[AssessmentRecord], threshold: float = 0.5) -> dict:
    rows = list(records)
    total = len(rows)
    verdicts = [classify_assessment(row, threshold) for row in rows]
    risk_counts = Counter(verdict.risk_status for verdict in verdicts)
    bucket_counts = Counter(score_to_bucket(row.score_decimal) for row in rows if row.score_decimal is not None)

    safe = risk_counts.get(RiskStatus.SAFE, 0)
    risk = risk_counts.get(RiskStatus.RISK, 0)
    unknown = risk_counts.get(RiskStatus.UNKNOWN, 0)

    summary = {
        "total_assessments": total,
        "safe_threshold": threshold,
        "safe_assessments": safe,
        "risk_assessments": risk,
        "unknown_assessments": unknown,
        "safe_rate": round((safe / total) * 100, 2) if total else 0,
        "risk_rate": round((risk / total) * 100, 2) if total else 0,
        "unknown_rate": round((unknown / total) * 100, 2) if total else 0,
    }
    for bucket in range(0, 11):
        summary[f"score_{bucket}_count"] = bucket_counts.get(bucket, 0)
    return summary
