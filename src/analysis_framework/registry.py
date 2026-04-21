from __future__ import annotations

from collections.abc import Callable

from analysis_framework.exceptions import RegistryError


AlgorithmFactory = Callable[[], object]


class AlgorithmRegistry:
    def __init__(self) -> None:
        self._algorithms: dict[str, AlgorithmFactory] = {}

    def register(self, name: str, factory: AlgorithmFactory) -> None:
        key = name.strip()
        if not key:
            raise RegistryError("Algorithm name must not be empty.")
        self._algorithms[key] = factory

    def create(self, name: str) -> object:
        try:
            return self._algorithms[name]()
        except KeyError as exc:
            available = ", ".join(sorted(self._algorithms)) or "none"
            raise RegistryError(
                f"Unknown algorithm '{name}'. Available algorithms: {available}."
            ) from exc

    def names(self) -> list[str]:
        return sorted(self._algorithms)

