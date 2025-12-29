#!/bin/bash
set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$PROJECT_ROOT/backend/.venv/bin/activate"
export PYTHONPATH="$PROJECT_ROOT/backend:$PYTHONPATH"

docker compose up -d
sleep 5
python3 -m pytest "$PROJECT_ROOT/backend/tests/"
docker compose down
