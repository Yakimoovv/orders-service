#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
echo "--> ruff check"
ruff check .
echo "--> ruff format --check ."
ruff format --check .
echo "--> mypy"
mypy orders
echo "--> pytest"
pytest
echo "All checks passed"

