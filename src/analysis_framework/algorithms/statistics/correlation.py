from __future__ import annotations

from itertools import combinations
from math import sqrt

from analysis_framework.algorithms.statistics.descriptive import _numeric_columns
from analysis_framework.core.base import BaseAlgorithm


def _pearson(x_values: list[float], y_values: list[float]) -> float:
    x_mean = sum(x_values) / len(x_values)
    y_mean = sum(y_values) / len(y_values)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values))
    x_denominator = sqrt(sum((x - x_mean) ** 2 for x in x_values))
    y_denominator = sqrt(sum((y - y_mean) ** 2 for y in y_values))
    if x_denominator == 0 or y_denominator == 0:
        return 0.0
    return round(numerator / (x_denominator * y_denominator), 4)


class CorrelationAlgorithm(BaseAlgorithm):
    name = "correlation"

    def run(self, data: list[dict], params: dict, context: dict) -> dict:
        numeric = _numeric_columns(data)
        correlations = {}
        for left, right in combinations(numeric.keys(), 2):
            correlations[f"{left}__{right}"] = _pearson(numeric[left], numeric[right])

        return {"data": data, "artifacts": correlations}

