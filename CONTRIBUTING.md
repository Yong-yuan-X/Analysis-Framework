# Contributing

Thanks for your interest in contributing to Analysis-Framework! This guide will help you get started.

## Getting Started

1. Fork and clone the repository:

   ```bash
   git clone https://github.com/<your-username>/Analysis-Framework.git
   cd Analysis-Framework
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Verify the setup by running the tests:

   ```bash
   python3 -m pytest -q
   ```

## Making Changes

1. Create a new branch for your work:

   ```bash
   git checkout -b your-feature-name
   ```

2. Make your changes in small, focused commits.

3. Run the tests before pushing:

   ```bash
   python3 -m pytest -q
   ```

4. You can also validate a pipeline config to make sure it still works:

   ```bash
   python3 scripts/run_pipeline.py validate --config configs/pipelines/basic_analysis.yaml
   ```

## Opening Issues and Pull Requests

- If you find a bug or have a feature idea, please open an issue first to discuss it.
- When opening a pull request, link it to the related issue if one exists.
- Keep pull requests small and focused on a single change.
- Make sure all tests pass before requesting a review.

## Project Overview

This is a modular data analysis framework. The core code lives in `src/analysis_framework/`, configuration files are in `configs/`, and tests are in `tests/`. See the [README](README.md) for a full overview of the project structure and available algorithms.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
