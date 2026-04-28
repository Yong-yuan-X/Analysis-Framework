# Analysis-Framework

[English](./README.md) | [简体中文](./README.zh-CN.md) | [繁體中文](./README.zh-HK.md)

This is a data analysis framework that includes a set of common algorithms and standardized workflows. Users can customize and adjust algorithms, and toggle them on or off as needed, providing a flexible, modular approach to data processing tasks.

This document describes the current local version of the project. It reflects what is already implemented and runnable in the repository today, not a future roadmap draft.

## Current Status

This repository is already a minimal runnable data analysis framework `MVP` with support for:

- reading raw `CSV` data
- defining analysis pipelines through configuration files
- executing built-in algorithms step by step
- writing processed output data files
- writing summary `JSON` analysis reports
- running from the command line, validating configs, and listing available algorithms

The framework currently includes 4 built-in algorithms:

1. `missing_values`
2. `descriptive_stats`
3. `categorical_frequency`
4. `correlation`

## Current Directory Structure

```text
Analysis-Framework/
├── README.md
├── README.zh-CN.md
├── README.zh-HK.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── .env.example
├── main.py
├── configs/
│   ├── default.yaml
│   └── pipelines/
│       └── basic_analysis.yaml
├── data/
│   ├── raw/
│   │   └── example.csv
│   └── processed/
│       ├── processed.csv
│       └── report.json
├── examples/
│   └── run_basic_analysis.py
├── scripts/
│   ├── run_pipeline.py
│   └── validate_config.py
├── tests/
│   ├── conftest.py
│   ├── test_pipeline.py
│   └── test_registry.py
└── src/
    └── analysis_framework/
        ├── __init__.py
        ├── cli.py
        ├── constants.py
        ├── exceptions.py
        ├── logging.py
        ├── registry.py
        ├── config/
        │   ├── __init__.py
        │   ├── loader.py
        │   └── schema.py
        ├── core/
        │   ├── __init__.py
        │   ├── base.py
        │   ├── pipeline.py
        │   └── result.py
        ├── dataio/
        │   ├── __init__.py
        │   ├── readers.py
        │   └── writers.py
        └── algorithms/
            ├── __init__.py
            ├── preprocessing/
            │   ├── __init__.py
            │   └── missing_values.py
            └── statistics/
                ├── __init__.py
                ├── correlation.py
                └── descriptive.py
```

## What Each Part Does

### Root Directory

- `README.md`
  Default English project overview.

- `README.zh-CN.md`
  Simplified Chinese project overview.

- `README.zh-HK.md`
  Traditional Chinese project overview.

- `pyproject.toml`
  Python project configuration, including package metadata and CLI entry points.

- `requirements.txt`
  Dependency list.

- `.env.example`
  Example local environment variables.

- `main.py`
  A simple welcome entry point that is not part of the main workflow yet.

### `configs/`

- `default.yaml`
  Default configuration example.

- `pipelines/basic_analysis.yaml`
  Runnable configuration for the current basic analysis pipeline.

Note:
Although these files use the `.yaml` extension, the current content is written in a `JSON`-compatible format so it can still run in environments without `PyYAML`.

### `data/`

- `data/raw/example.csv`
  Raw input data.

- `data/processed/processed.csv`
  Processed output data produced by the pipeline.

- `data/processed/report.json`
  Summary report for the pipeline execution.

The relationship is:

- `raw` is the input
- `processed.csv` is the output data
- `report.json` is the output report

### `scripts/`

- `scripts/run_pipeline.py`
  Main execution entry point.

- `scripts/validate_config.py`
  Configuration validation entry point.

### `src/analysis_framework/`

This is the core framework code.

- `cli.py`
  Command-line parsing for `run`, `validate`, and `list-algorithms`.

- `registry.py`
  Algorithm registry responsible for registering and instantiating algorithms.

- `config/loader.py`
  Loads configuration files.

- `config/schema.py`
  Validates whether a configuration is legal.

- `core/base.py`
  Base class definition for algorithms.

- `core/pipeline.py`
  Pipeline orchestration core that runs algorithms in configured order.

- `core/result.py`
  Defines the pipeline result object.

- `dataio/readers.py`
  Reads `CSV` data.

- `dataio/writers.py`
  Writes `CSV` and `JSON` output files.

- `algorithms/preprocessing/missing_values.py`
  Missing-value handling algorithm.

- `algorithms/statistics/descriptive.py`
  Descriptive statistics algorithm.

- `algorithms/statistics/frequency.py`
  Categorical frequency statistics algorithm.

- `algorithms/statistics/correlation.py`
  Correlation analysis algorithm.

## Implemented Features

### 1. CSV Data Loading

The framework currently supports loading raw data from `CSV` files such as:

```text
data/raw/example.csv
```

### 2. Configuration-Driven Pipeline Execution

The current pipeline is controlled by a configuration file. An example is available at:

```text
configs/pipelines/basic_analysis.yaml
```

This configuration defines:

- the input file path
- which steps to run
- whether each step is enabled
- the parameters for each step
- the output directory

### 3. Missing Value Handling Algorithm `missing_values`

Purpose:
Handle empty values in the raw data to reduce downstream analysis errors.

Currently supported strategy:

- `mean`

In the sample data:

- `age` has missing values
- `income` has missing values

After running the pipeline, those values are filled with the column mean.

### 4. Descriptive Statistics Algorithm `descriptive_stats`

Purpose:
Generate basic statistical summaries for numeric columns.

Current output metrics include:

- `count`
- `min`
- `max`
- `mean`

### 5. Categorical Frequency Algorithm `categorical_frequency`

Purpose:
Summarize value frequencies for categorical columns to help identify common categories and basic data distribution.

Current output includes:

- `total`: number of non-empty values in the column
- `unique`: number of distinct values
- `top_values`: the most common values with count and ratio

By default, the sample pipeline analyzes the `city` column and keeps the top `3` values.

### 6. Correlation Analysis Algorithm `correlation`

Purpose:
Compute Pearson correlation coefficients between numeric columns to help observe linear relationships.

Interpretation:

- close to `1`: strong positive correlation
- close to `0`: weak correlation
- close to `-1`: strong negative correlation

### 7. Processed Data Output

After the pipeline finishes, it produces:

```text
data/processed/processed.csv
```

This represents the processed dataset, for example with missing values already filled in.

### 8. Analysis Report Output

After the pipeline finishes, it also produces:

```text
data/processed/report.json
```

This file currently contains:

- the pipeline name `pipeline`
- the steps actually executed `executed_steps`
- a summary of artifacts generated by each step `artifacts`

### 9. Command-Line Capabilities

The framework currently supports 3 commands:

- `run`
- `validate`
- `list-algorithms`

## Usage

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Validate the Configuration

```bash
python3 scripts/run_pipeline.py validate --config configs/pipelines/basic_analysis.yaml
```

### List Available Algorithms

```bash
python3 scripts/run_pipeline.py list-algorithms
```

### Run the Analysis Pipeline

```bash
python3 scripts/run_pipeline.py run --config configs/pipelines/basic_analysis.yaml
```

### Inspect the Results

After running, you will have:

- [example.csv](/Users/a1-6/Analysis-Framework/data/raw/example.csv)
- [processed.csv](/Users/a1-6/Analysis-Framework/data/processed/processed.csv)
- [report.json](/Users/a1-6/Analysis-Framework/data/processed/report.json)

Their relationship is:

- `example.csv` is the raw data
- `processed.csv` is the processed data
- `report.json` is the analysis summary

## Current Test Status

There are already basic tests:

- [test_registry.py](/Users/a1-6/Analysis-Framework/tests/test_registry.py)
- [test_pipeline.py](/Users/a1-6/Analysis-Framework/tests/test_pipeline.py)

Verified locally with:

```bash
python3 -m pytest -q
```

## Current Limitations

This is still a minimal version, with the following limitations:

- only `CSV` input is supported
- there are only 4 built-in algorithms
- descriptive statistics are still basic
- there is no visualization output yet
- there is no plugin system or broader data source support yet

## Good Next Expansion Directions

Suitable next steps for the project include:

1. missing rate statistics
2. median, standard deviation, and quantiles
3. normalization / standardization
4. outlier detection
5. Excel / JSON input support
