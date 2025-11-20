#!/bin/bash
set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

trap "$PROJECT_ROOT/scripts/exit.sh" EXIT
source "$PROJECT_ROOT/backend/.venv/bin/activate"

# Run in a subshell so cd doesn't affect parent process
(
  cd "$PROJECT_ROOT"
  docker compose up -d

  cd "$PROJECT_ROOT/backend"
  python3 run.py &

  cd "$PROJECT_ROOT/frontend"
  npm run dev
)
