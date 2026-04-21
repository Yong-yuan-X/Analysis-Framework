class AnalysisFrameworkError(Exception):
    """Base exception for framework errors."""


class ConfigError(AnalysisFrameworkError):
    """Raised when configuration is invalid."""


class RegistryError(AnalysisFrameworkError):
    """Raised when algorithm lookup or registration fails."""


class PipelineError(AnalysisFrameworkError):
    """Raised when pipeline execution fails."""

