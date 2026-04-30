from analysis_framework.algorithms.preprocessing.missing_values import MissingValuesAlgorithm
from analysis_framework.algorithms.statistics.correlation import CorrelationAlgorithm
from analysis_framework.algorithms.statistics.frequency import CategoricalFrequencyAlgorithm
from analysis_framework.algorithms.statistics.descriptive import DescriptiveStatsAlgorithm
from analysis_framework.registry import AlgorithmRegistry


def register_builtin_algorithms(registry: AlgorithmRegistry) -> None:
    registry.register("missing_values", MissingValuesAlgorithm)
    registry.register("descriptive_stats", DescriptiveStatsAlgorithm)
    registry.register("categorical_frequency", CategoricalFrequencyAlgorithm)
    registry.register("correlation", CorrelationAlgorithm)
