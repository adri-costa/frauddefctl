from __future__ import annotations

import re
from pathlib import Path

_SPLIT_RE = re.compile(r"[;,\t\n\r ]+")


def parse_many(raw: str | None = None, file_path: str | Path | None = None) -> list[str]:
    """Normalize valores colados de Excel, logs, CSV simples ou linhas de texto.

    Aceita vírgula, ponto e vírgula, tab, espaço e quebra de linha.
    Remove vazios, aspas simples/duplas nas bordas e duplicados preservando a ordem.
    """
    chunks: list[str] = []

    if raw:
        chunks.append(raw)

    if file_path:
        chunks.append(Path(file_path).read_text(encoding="utf-8"))

    seen: set[str] = set()
    values: list[str] = []
    for item in _SPLIT_RE.split("\n".join(chunks)):
        normalized = item.strip().strip("'\"")
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        values.append(normalized)

    return values
