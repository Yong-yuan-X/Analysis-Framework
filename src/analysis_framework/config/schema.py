from __future__ import annotations

from analysis_framework.exceptions import ConfigError


def validate_config(config: dict) -> None:
    if "input" not in config:
        raise ConfigError("Missing required 'input' section.")
    if "steps" not in config or not isinstance(config["steps"], list) or not config["steps"]:
        raise ConfigError("Missing required non-empty 'steps' list.")

    input_config = config["input"]
    if input_config.get("type") != "csv":
        raise ConfigError("MVP currently supports only input.type = 'csv'.")
    if not input_config.get("path"):
        raise ConfigError("input.path is required.")

    for index, step in enumerate(config["steps"], start=1):
        if not isinstance(step, dict):
            raise ConfigError(f"Step #{index} must be a mapping.")
        if not step.get("name"):
            raise ConfigError(f"Step #{index} is missing 'name'.")

