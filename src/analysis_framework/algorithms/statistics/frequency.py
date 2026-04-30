from __future__ import annotations

from collections import Counter

from analysis_framework.core.base import BaseAlgorithm


def _is_number(value: str) -> bool:
    try:
        float(value)
    except (TypeError, ValueError):
        return False
    return True


def _default_categorical_columns(data: list[dict]) -> list[str]:
    if not data:
        return []

    columns = []
    for column in data[0]:
        values = [row.get(column) for row in data if row.get(column) not in (None, "")]
        if values and any(not _is_number(value) for value in values):
            columns.append(column)
    return columns


class CategoricalFrequencyAlgorithm(BaseAlgorithm):
    name = "categorical_frequency"

    def run(self, data: list[dict], params: dict, context: dict) -> dict:
        columns = params.get("columns") or _default_categorical_columns(data)
        top_n = int(params.get("top_n", 3))
        artifacts = {}

        for column in columns:
            values = [row.get(column) for row in data if row.get(column) not in (None, "")]
            counts = Counter(values)
            total = sum(counts.values())
            artifacts[column] = {
                "total": total,
                "unique": len(counts),
                "top_values": [
                    {
                        "value": value,
                        "count": count,
                        "ratio": round(count / total, 4) if total else 0.0,
                    }
                    for value, count in counts.most_common(top_n)
                ],
            }

        return {"data": data, "artifacts": artifacts}
