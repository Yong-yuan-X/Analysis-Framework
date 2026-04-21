from __future__ import annotations

import csv
from pathlib import Path

from analysis_framework.exceptions import PipelineError


def read_csv(path: str) -> list[dict]:
    csv_path = Path(path)
    if not csv_path.exists():
        raise PipelineError(f"Input file not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise PipelineError(f"Input file has no data rows: {csv_path}")

    if not rows[0]:
        raise PipelineError(f"Input file is missing a valid header row: {csv_path}")

    return rows
