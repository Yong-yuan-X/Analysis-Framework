from __future__ import annotations

from analysis_framework.core.base import BaseAlgorithm


def _numeric_columns(data: list[dict]) -> dict[str, list[float]]:
    numeric: dict[str, list[float]] = {}
    if not data:
        return numeric

    for column in data[0]:
        values: list[float] = []
        for row in data:
            value = row.get(column)
            try:
                if value not in (None, ""):
                    values.append(float(value))
            except (TypeError, ValueError):
                values = []
                break
        if values:
            numeric[column] = values
    return numeric


class DescriptiveStatsAlgorithm(BaseAlgorithm):
    name = "descriptive_stats"

    def run(self, data: list[dict], params: dict, context: dict) -> dict:
        stats = {}
        for column, values in _numeric_columns(data).items():
            stats[column] = {
                "count": len(values),
                "min": min(values),
                "max": max(values),
                "mean": round(sum(values) / len(values), 4),
            }

        return {"data": data, "artifacts": stats}

