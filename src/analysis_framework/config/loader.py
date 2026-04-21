from __future__ import annotations

import json
from pathlib import Path

from analysis_framework.config.schema import validate_config
from analysis_framework.exceptions import ConfigError

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - exercised in environments without PyYAML
    yaml = None


def load_config(path: str | Path) -> dict:
    config_path = Path(path)
    if not config_path.exists():
        raise ConfigError(f"Config file does not exist: {config_path}")

    with config_path.open("r", encoding="utf-8") as handle:
        content = handle.read()

    if yaml is not None:
        data = yaml.safe_load(content) or {}
    else:
        data = json.loads(content)

    if not isinstance(data, dict):
        raise ConfigError("Config root must be a mapping.")

    validate_config(data)
    return data
