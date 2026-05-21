# Analysis-Framework

[English](./README.md) | [简体中文](./README.zh-CN.md)

A lightweight local tool for profiling tabular datasets and generating structured analysis reports. Load your data, run a configurable pipeline, and get quality checks, summary statistics, and a clean JSON report — all from the command line.

This document describes the current local version of the project. It reflects what is already implemented and runnable in the repository today.

## What It Does

- **Data quality checks** — detect and fill missing values
- **Basic statistics** — descriptive stats (count, min, max, mean) for numeric columns
- **Categorical profiling** — frequency distribution for categorical columns
- **Correlation analysis** — Pearson correlation between numeric columns
- **Configurable pipelines** — define which analysis steps to run via YAML config files
- **Structured reports** — outputs a JSON summary report alongside processed CSV data

## Supported Input Formats

CSV, JSON, XLSX, and SQLite. All inputs are normalized into a consistent row format before the pipeline runs.

## Quick Start

### Install

```bash
pip install -r requirements.txt
```

### Validate a Config

```bash
python3 scripts/run_pipeline.py validate --config configs/pipelines/basic_analysis.yaml
```

### Run a Pipeline

```bash
python3 scripts/run_pipeline.py run --config configs/pipelines/basic_analysis.yaml
```

To run with JSON input instead:

```bash
python3 scripts/run_pipeline.py run --config configs/pipelines/json_analysis.yaml
```

### List Available Algorithms

```bash
python3 scripts/run_pipeline.py list-algorithms
```

## Output

After a pipeline run you get:

| File | Description |
|------|-------------|
| `data/processed/processed.csv` | Cleaned dataset (e.g. missing values filled) |
| `data/processed/report.json` | Structured analysis report |

## Built-in Algorithms

| Algorithm | Purpose |
|-----------|---------|
| `missing_values` | Fill missing values (currently supports mean imputation) |
| `descriptive_stats` | Count, min, max, mean for numeric columns |
| `categorical_frequency` | Value counts and top-N frequencies for categorical columns |
| `correlation` | Pearson correlation matrix for numeric columns |

## Configuration

Pipelines are defined in YAML config files under `configs/pipelines/`. Each config specifies:

- input file path and format
- which steps to run and their parameters
- output directory

See `configs/pipelines/basic_analysis.yaml` for a working example.

## Directory Structure

```text
Analysis-Framework/
├── configs/               # Pipeline configuration files
│   └── pipelines/
├── data/
│   ├── raw/               # Input data
│   └── processed/         # Output data and reports
├── examples/              # Usage examples
├── scripts/               # CLI entry points
├── src/analysis_framework/
│   ├── algorithms/        # Built-in analysis algorithms
│   ├── config/            # Config loading and validation
│   ├── core/              # Pipeline orchestration
│   └── dataio/            # Data readers and writers
└── tests/
```

## Current Limitations

- Only CSV, JSON, XLSX, and SQLite inputs are supported
- 4 built-in algorithms; descriptive statistics are still basic
- No visualization output yet

## License

See [LICENSE](./LICENSE).
