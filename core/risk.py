from __future__ import annotations

from frauddefctl.core.models import AssessmentRecord, AssessmentVerdict, RiskStatus


def score_to_bucket(score: float | None) -> int | None:
    if score is None:
        return None
    return int(round(score * 10))


def classify_score(score: float | None, threshold: float = 0.5) -> RiskStatus:
    if score is None:
        return RiskStatus.UNKNOWN
    if score >= threshold:
        return RiskStatus.SAFE
    return RiskStatus.RISK


def classify_assessment(record: AssessmentRecord, threshold: float = 0.5) -> AssessmentVerdict:
    return AssessmentVerdict(
        assessment_id=record.assessment_id,
        score_decimal=record.score_decimal,
        score_bucket=score_to_bucket(record.score_decimal),
        risk_status=classify_score(record.score_decimal, threshold),
        threshold=threshold,
    )
