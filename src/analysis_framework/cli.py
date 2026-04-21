from __future__ import annotations

import argparse
import json
import sys

from analysis_framework.algorithms import register_builtin_algorithms
from analysis_framework.config import load_config, validate_config
from analysis_framework.constants import DEFAULT_PIPELINE_CONFIG
from analysis_framework.core import PipelineRunner
from analysis_framework.exceptions import AnalysisFrameworkError
from analysis_framework.logging import configure_logging
from analysis_framework.registry import AlgorithmRegistry


def build_registry() -> AlgorithmRegistry:
    registry = AlgorithmRegistry()
    register_builtin_algorithms(registry)
    return registry


def cmd_run(args: argparse.Namespace) -> int:
    try:
        config = load_config(args.config)
        configure_logging()
        runner = PipelineRunner(build_registry())
        result = runner.run(config)
        print(
            json.dumps(
                {"executed_steps": result.executed_steps, "artifacts": result.artifacts},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    except AnalysisFrameworkError as exc:
        print("Pipeline failed", file=sys.stderr)
        print(f"Config: {args.config}", file=sys.stderr)
        print(f"Reason: {exc}", file=sys.stderr)
        return 1


def cmd_validate(args: argparse.Namespace) -> int:
    try:
        config = load_config(args.config)
        validate_config(config)
        print(f"Config is valid: {args.config}")
        return 0
    except AnalysisFrameworkError as exc:
        print("Config validation failed", file=sys.stderr)
        print(f"Config: {args.config}", file=sys.stderr)
        print(f"Reason: {exc}", file=sys.stderr)
        return 1


def cmd_list_algorithms(args: argparse.Namespace) -> int:
    registry = build_registry()
    for name in registry.names():
        print(name)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="analysis-framework")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a pipeline config.")
    run_parser.add_argument("--config", default=DEFAULT_PIPELINE_CONFIG)
    run_parser.set_defaults(func=cmd_run)

    validate_parser = subparsers.add_parser("validate", help="Validate a pipeline config.")
    validate_parser.add_argument("--config", default=DEFAULT_PIPELINE_CONFIG)
    validate_parser.set_defaults(func=cmd_validate)

    list_parser = subparsers.add_parser("list-algorithms", help="List registered algorithms.")
    list_parser.set_defaults(func=cmd_list_algorithms)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
