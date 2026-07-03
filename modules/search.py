from __future__ import annotations

import ipaddress
from urllib.parse import urlparse


def detect_search_type(value: str) -> str:
    candidate = value.strip()
    if not candidate:
        return "empty"
    if candidate.startswith("http://") or candidate.startswith("https://"):
        return "url"
    try:
        ipaddress.ip_network(candidate, strict=False)
        return "ip_or_cidr"
    except ValueError:
        pass
    if candidate.startswith("6L"):
        return "site_key_id"
    if "." in candidate and " " not in candidate:
        return "domain"
    return "name"


def normalize_search_value(value: str) -> str:
    search_type = detect_search_type(value)
    if search_type == "url":
        return urlparse(value).hostname or value
    return value.strip()
