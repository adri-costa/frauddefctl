from __future__ import annotations

from pathlib import Path

import yaml

from frauddefctl.core.models import FraudDefCtlConfig


DEFAULT_CONFIG_PATH = Path("config/config.example.yaml")


class ConfigError(RuntimeError):
    pass


def load_config(path: str | Path | None = None) -> FraudDefCtlConfig:
    config_path = Path(path) if path else DEFAULT_CONFIG_PATH
    if not config_path.exists():
        raise ConfigError(f"Arquivo de configuração não encontrado: {config_path}")

    with config_path.open("r", encoding="utf-8") as fp:
        data = yaml.safe_load(fp) or {}

    try:
        return FraudDefCtlConfig.model_validate(data)
    except Exception as exc:  # pydantic ValidationError plus YAML edge cases
        raise ConfigError(f"Configuração inválida em {config_path}: {exc}") from exc


def enabled_projects(config: FraudDefCtlConfig) -> list[str]:
    return [project.project_id for project in config.projects if project.enabled]
