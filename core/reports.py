from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo


def timestamp(timezone: str = "America/Sao_Paulo") -> str:
    return datetime.now(ZoneInfo(timezone)).strftime("%Y%m%d_%H%M%S")


def ensure_output_dir(path: str | Path) -> Path:
    output_dir = Path(path)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def export_json(records: Iterable[dict], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fp:
        json.dump(list(records), fp, ensure_ascii=False, indent=2)
    return path


def export_csv(records: Iterable[dict], output_path: str | Path, separator: str = ";") -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = list(records)
    fieldnames = sorted({key for row in rows for key in row.keys()}) if rows else []
    with path.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames, delimiter=separator, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    return path


def export_markdown(records: Iterable[dict], output_path: str | Path, title: str) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = list(records)
    with path.open("w", encoding="utf-8") as fp:
        fp.write(f"# {title}\n\n")
        if not rows:
            fp.write("Nenhum registro encontrado.\n")
            return path
        columns = sorted({key for row in rows for key in row.keys()})
        fp.write("| " + " | ".join(columns) + " |\n")
        fp.write("| " + " | ".join(["---"] * len(columns)) + " |\n")
        for row in rows:
            fp.write("| " + " | ".join(str(row.get(col, "")) for col in columns) + " |\n")
    return path
