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

    assert result.executed_steps == [
        "missing_values",
        "descriptive_stats",
        "categorical_frequency",
        "correlation",
    ]
    assert (tmp_path / "processed.csv").exists()
    report = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    assert report["pipeline"] == "basic_analysis"
    assert report["artifacts"]["categorical_frequency"]["city"]["unique"] == 5


def test_pipeline_runs_with_json_input(tmp_path):
    input_path = tmp_path / "input.json"
    input_path.write_text(
        json.dumps(
            [
                {"id": "1", "age": "25", "income": "5000", "score": "80", "city": "Shanghai"},
                {"id": "2", "age": "", "income": "6200", "score": "88", "city": "Beijing"},
                {"id": "3", "age": "35", "income": "7100", "score": "93", "city": "Shanghai"},
            ]
        ),
        encoding="utf-8",
    )
    config = load_config("configs/pipelines/basic_analysis.yaml")
    config["input"] = {"type": "json", "path": str(input_path)}
    config["output"]["dir"] = str(tmp_path)

    registry = AlgorithmRegistry()
    register_builtin_algorithms(registry)
    result = PipelineRunner(registry).run(config)

    assert result.executed_steps == [
        "missing_values",
        "descriptive_stats",
        "categorical_frequency",
        "correlation",
    ]
    assert result.artifacts["missing_values"]["filled_columns"] == ["age", "id", "income", "score"]
    assert result.artifacts["categorical_frequency"]["city"]["top_values"][0]["value"] == "Shanghai"
