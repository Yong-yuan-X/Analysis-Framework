from __future__ import annotations

from analysis_framework.core.base import BaseAlgorithm


def _to_float(value: str) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


class MissingValuesAlgorithm(BaseAlgorithm):
    name = "missing_values"

    def run(self, data: list[dict], params: dict, context: dict) -> dict:
        strategy = params.get("strategy", "constant")
        columns = data[0].keys() if data else []
        numeric_fill_values: dict[str, str] = {}

        if strategy == "mean":
            for column in columns:
                values = [_to_float(row.get(column)) for row in data]
                numeric_values = [value for value in values if value is not None]
                if numeric_values:
                    numeric_fill_values[column] = str(round(sum(numeric_values) / len(numeric_values), 4))

        filled = []
        for row in data:
            updated = {}
            for key, value in row.items():
                if value not in (None, ""):
                    updated[key] = value
                elif key in numeric_fill_values:
                    updated[key] = numeric_fill_values[key]
                else:
                    updated[key] = str(params.get("fill_value", "unknown"))
            filled.append(updated)

        return {
            "data": filled,
            "artifacts": {
                "strategy": strategy,
                "filled_columns": sorted(numeric_fill_values),
            },
        }

