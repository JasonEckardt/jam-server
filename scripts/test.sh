#!/bin/bash
set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$PROJECT_ROOT/backend/.venv/bin/activate"
export PYTHONPATH="$PROJECT_ROOT/backend:$PYTHONPATH"

python3 -m pytest "$PROJECT_ROOT/backend/tests/"
