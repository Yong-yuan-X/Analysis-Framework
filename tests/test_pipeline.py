import json

from analysis_framework.algorithms import register_builtin_algorithms
from analysis_framework.config import load_config
from analysis_framework.core import PipelineRunner
from analysis_framework.registry import AlgorithmRegistry


def test_pipeline_runs_end_to_end(tmp_path):
    config = load_config("configs/pipelines/basic_analysis.yaml")
    config["output"]["dir"] = str(tmp_path)

    registry = AlgorithmRegistry()
    register_builtin_algorithms(registry)
    result = PipelineRunner(registry).run(config)

    assert result.executed_steps == ["missing_values", "descriptive_stats", "correlation"]
    assert (tmp_path / "processed.csv").exists()
    report = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    assert report["pipeline"] == "basic_analysis"

