from __future__ import annotations

from abc import ABC, abstractmethod


class BaseAlgorithm(ABC):
    """Abstract base class for all pipeline algorithms."""

    name = "base"

    @abstractmethod
    def run(self, data: list[dict], params: dict, context: dict) -> dict:
        """Execute an algorithm step and return structured outputs."""

