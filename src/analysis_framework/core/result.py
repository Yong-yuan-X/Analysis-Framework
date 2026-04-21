from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PipelineResult:
    data: list[dict]
    artifacts: dict = field(default_factory=dict)
    executed_steps: list[str] = field(default_factory=list)

