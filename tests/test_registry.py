from analysis_framework.algorithms import register_builtin_algorithms
from analysis_framework.registry import AlgorithmRegistry


def test_builtin_algorithms_are_registered():
    registry = AlgorithmRegistry()
    register_builtin_algorithms(registry)

    assert registry.names() == ["correlation", "descriptive_stats", "missing_values"]

