from __future__ import annotations

import logging

from analysis_framework.core.result import PipelineResult
from analysis_framework.dataio.readers import read_csv
from analysis_framework.dataio.writers import write_csv, write_json
from analysis_framework.exceptions import PipelineError
from analysis_framework.registry import AlgorithmRegistry


class PipelineRunner:
    def __init__(self, registry: AlgorithmRegistry) -> None:
        self.registry = registry
        self.logger = logging.getLogger(self.__class__.__name__)

    def run(self, config: dict) -> PipelineResult:
        input_path = config["input"]["path"]
        try:
            data = read_csv(input_path)
        except Exception as exc:
            if isinstance(exc, PipelineError):
                raise
            raise PipelineError(f"Failed to read input data: {input_path}. Reason: {exc}") from exc

        artifacts: dict = {}
        executed_steps: list[str] = []
        context = {"pipeline_name": config.get("name", "unnamed")}

        for step in config["steps"]:
            if not step.get("enabled", True):
                continue

            name = step["name"]
            params = step.get("params", {})
            algorithm = self.registry.create(name)
            self.logger.info("Running step '%s'", name)
            try:
                result = algorithm.run(data=data, params=params, context=context)
            except Exception as exc:
                raise PipelineError(f"Step '{name}' failed. Reason: {exc}") from exc

            if not isinstance(result, dict) or "data" not in result:
                raise PipelineError(f"Algorithm '{name}' returned an invalid result.")

            data = result["data"]
            step_artifacts = result.get("artifacts", {})
            if step_artifacts:
                artifacts[name] = step_artifacts
            executed_steps.append(name)

        output_dir = config.get("output", {}).get("dir", "data/processed")
        try:
            if config.get("output", {}).get("save_processed", True):
                write_csv(f"{output_dir}/processed.csv", data)
            if config.get("output", {}).get("save_report", True):
                write_json(
                    f"{output_dir}/report.json",
                    {
                        "pipeline": context["pipeline_name"],
                        "executed_steps": executed_steps,
                        "artifacts": artifacts,
                    },
                )
        except Exception as exc:
            raise PipelineError(f"Failed to write pipeline outputs. Reason: {exc}") from exc

        return PipelineResult(data=data, artifacts=artifacts, executed_steps=executed_steps)
