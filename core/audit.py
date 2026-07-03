from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def write_audit_log(
    *,
    command: str,
    actor: str | None,
    mode: str,
    result: str,
    project_id: str | None = None,
    resource_id: str | None = None,
    dry_run: bool = True,
    reason: str | None = None,
    audit_dir: str | Path = "logs/audit",
    timezone: str = "America/Sao_Paulo",
) -> Path:
    path = Path(audit_dir)
    path.mkdir(parents=True, exist_ok=True)
    now = datetime.now(ZoneInfo(timezone))
    record = {
        "timestamp": now.isoformat(),
        "actor": actor,
        "mode": mode,
        "command": command,
        "project_id": project_id,
        "resource_id": resource_id,
        "dry_run": dry_run,
        "result": result,
        "reason": reason,
    }
    filename = path / f"audit_{now.strftime('%Y%m%d')}.jsonl"
    with filename.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(record, ensure_ascii=False) + "\n")
    return filename
