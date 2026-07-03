from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GuardrailDecision:
    allowed: bool
    reason: str


def can_delete_resource(*, dry_run: bool, force: bool, has_recent_traffic: bool) -> GuardrailDecision:
    if dry_run:
        return GuardrailDecision(True, "dry_run")
    if has_recent_traffic and not force:
        return GuardrailDecision(False, "resource_has_recent_traffic")
    if not force:
        return GuardrailDecision(False, "force_required")
    return GuardrailDecision(True, "allowed")
